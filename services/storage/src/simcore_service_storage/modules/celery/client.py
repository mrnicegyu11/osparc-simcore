import contextlib
import logging
from dataclasses import dataclass
from typing import Any, Final
from uuid import uuid4

from celery import Celery  # type: ignore[import-untyped]
from celery.contrib.abortable import (  # type: ignore[import-untyped]
    AbortableAsyncResult,
)
from common_library.async_tools import make_async
from models_library.progress_bar import ProgressReport
from pydantic import ValidationError
from servicelib.logging_utils import log_context

from ...exceptions.errors import ConfigurationError
from .models import TaskContext, TaskID, TaskState, TaskStatus, TaskUUID

_logger = logging.getLogger(__name__)

_CELERY_INSPECT_TASK_STATUSES: Final[tuple[str, ...]] = (
    "active",
    "scheduled",
    "revoked",
)
_CELERY_TASK_META_PREFIX: Final[str] = "celery-task-meta-"
_CELERY_STATES_MAPPING: Final[dict[str, TaskState]] = {
    "PENDING": TaskState.PENDING,
    "STARTED": TaskState.PENDING,
    "RETRY": TaskState.PENDING,
    "RUNNING": TaskState.RUNNING,
    "SUCCESS": TaskState.SUCCESS,
    "ABORTED": TaskState.ABORTED,
    "FAILURE": TaskState.ERROR,
    "ERROR": TaskState.ERROR,
}
_CELERY_TASK_ID_KEY_SEPARATOR: Final[str] = ":"
_CELERY_TASK_ID_KEY_ENCODING = "utf-8"

_MIN_PROGRESS_VALUE = 0.0
_MAX_PROGRESS_VALUE = 1.0


def _build_context_prefix(task_context: TaskContext) -> list[str]:
    return [f"{task_context[key]}" for key in sorted(task_context)]


def _build_task_id_prefix(task_context: TaskContext) -> str:
    return _CELERY_TASK_ID_KEY_SEPARATOR.join(_build_context_prefix(task_context))


def _build_task_id(task_context: TaskContext, task_uuid: TaskUUID) -> TaskID:
    return _CELERY_TASK_ID_KEY_SEPARATOR.join(
        [_build_task_id_prefix(task_context), f"{task_uuid}"]
    )


@dataclass
class CeleryTaskQueueClient:
    _celery_app: Celery

    @make_async()
    def send_task(
        self, task_name: str, *, task_context: TaskContext, **task_params
    ) -> TaskUUID:
        with log_context(
            _logger,
            logging.DEBUG,
            msg=f"Submit {task_name=}: {task_context=} {task_params=}",
        ):
            task_uuid = uuid4()
            task_id = _build_task_id(task_context, task_uuid)
            self._celery_app.send_task(task_name, task_id=task_id, kwargs=task_params)
            return task_uuid

    @staticmethod
    @make_async()
    def abort_task(task_context: TaskContext, task_uuid: TaskUUID) -> None:
        with log_context(
            _logger,
            logging.DEBUG,
            msg=f"Abort task {task_uuid=}: {task_context=}",
        ):
            task_id = _build_task_id(task_context, task_uuid)
            AbortableAsyncResult(task_id).abort()

    @make_async()
    def get_task_result(self, task_context: TaskContext, task_uuid: TaskUUID) -> Any:
        with log_context(
            _logger,
            logging.DEBUG,
            msg=f"Get task {task_uuid=}: {task_context=} result",
        ):
            task_id = _build_task_id(task_context, task_uuid)
            return self._celery_app.AsyncResult(task_id).result

    def _get_progress_report(
        self, task_context: TaskContext, task_uuid: TaskUUID
    ) -> ProgressReport:
        task_id = _build_task_id(task_context, task_uuid)
        result = self._celery_app.AsyncResult(task_id).result
        state = self._get_state(task_context, task_uuid)
        if result and state == TaskState.RUNNING:
            with contextlib.suppress(ValidationError):
                # avoids exception if result is not a ProgressReport (or overwritten by a Celery's state update)
                return ProgressReport.model_validate(result)
        if state in (
            TaskState.ABORTED,
            TaskState.ERROR,
            TaskState.SUCCESS,
        ):
            return ProgressReport(
                actual_value=_MAX_PROGRESS_VALUE, total=_MAX_PROGRESS_VALUE
            )
        return ProgressReport(
            actual_value=_MIN_PROGRESS_VALUE, total=_MAX_PROGRESS_VALUE
        )

    def _get_state(self, task_context: TaskContext, task_uuid: TaskUUID) -> TaskState:
        task_id = _build_task_id(task_context, task_uuid)
        return _CELERY_STATES_MAPPING[self._celery_app.AsyncResult(task_id).state]

    @make_async()
    def get_task_status(
        self, task_context: TaskContext, task_uuid: TaskUUID
    ) -> TaskStatus:
        return TaskStatus(
            task_uuid=task_uuid,
            task_state=self._get_state(task_context, task_uuid),
            progress_report=self._get_progress_report(task_context, task_uuid),
        )

    def _get_completed_task_uuids(self, task_context: TaskContext) -> set[TaskUUID]:
        search_key = _CELERY_TASK_META_PREFIX + _build_task_id_prefix(task_context)
        backend_client = self._celery_app.backend.client
        if hasattr(backend_client, "keys") and (
            keys := backend_client.keys(f"{search_key}*")
        ):
            return {
                TaskUUID(
                    f"{key.decode(_CELERY_TASK_ID_KEY_ENCODING).removeprefix(search_key + _CELERY_TASK_ID_KEY_SEPARATOR)}"
                )
                for key in keys
            }
        if hasattr(backend_client, "cache"):
            # NOTE: backend used in testing. It is a dict-like object
            found_keys = set()
            for key in backend_client.cache:
                str_key = key.decode(_CELERY_TASK_ID_KEY_ENCODING)
                if str_key.startswith(search_key):
                    found_keys.add(
                        TaskUUID(
                            f"{str_key.removeprefix(search_key + _CELERY_TASK_ID_KEY_SEPARATOR)}"
                        )
                    )
            return found_keys
        msg = f"Unsupported backend {self._celery_app.backend.__class__.__name__}"
        raise ConfigurationError(msg=msg)

    @make_async()
    def get_task_uuids(self, task_context: TaskContext) -> set[TaskUUID]:
        task_uuids = self._get_completed_task_uuids(task_context)

        task_id_prefix = _build_task_id_prefix(task_context)
        inspect = self._celery_app.control.inspect()
        for task_inspect_status in _CELERY_INSPECT_TASK_STATUSES:
            tasks = getattr(inspect, task_inspect_status)() or {}

            task_uuids.update(
                TaskUUID(
                    task_info["id"].removeprefix(
                        task_id_prefix + _CELERY_TASK_ID_KEY_SEPARATOR
                    )
                )
                for tasks_per_worker in tasks.values()
                for task_info in tasks_per_worker
                if "id" in task_info
            )

        return task_uuids
