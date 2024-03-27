import functools
import logging
from dataclasses import dataclass
from typing import Final

from botocore import exceptions as botocore_exc
from pydantic import ByteSize, parse_obj_as
from servicelib.aiohttp.long_running_tasks.server import (
    ProgressMessage,
    ProgressPercent,
    TaskProgress,
)

from .exceptions import S3AccessError, S3BucketInvalidError, S3KeyNotFoundError

logger = logging.getLogger(__name__)

# this is artifically defined, if possible we keep a maximum number of requests for parallel
# uploading. If that is not possible then we create as many upload part as the max part size allows
_MULTIPART_UPLOADS_TARGET_MAX_PART_SIZE: Final[list[ByteSize]] = [
    parse_obj_as(ByteSize, x)
    for x in [
        "10Mib",
        "50Mib",
        "100Mib",
        "200Mib",
        "400Mib",
        "600Mib",
        "800Mib",
        "1Gib",
        "2Gib",
        "3Gib",
        "4Gib",
        "5Gib",
    ]
]
_MULTIPART_MAX_NUMBER_OF_PARTS: Final[int] = 10000


def compute_num_file_chunks(file_size: ByteSize) -> tuple[int, ByteSize]:
    for chunk in _MULTIPART_UPLOADS_TARGET_MAX_PART_SIZE:
        num_upload_links = int(file_size / chunk) + (1 if file_size % chunk > 0 else 0)
        if num_upload_links < _MULTIPART_MAX_NUMBER_OF_PARTS:
            return (num_upload_links, chunk)
    raise ValueError(
        f"Could not determine number of upload links for {file_size=}",
    )


def s3_exception_handler(log: logging.Logger):
    """converts typical aiobotocore/boto exceptions to storage exceptions
    NOTE: this is a work in progress as more exceptions might arise in different
    use-cases
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                response = await func(self, *args, **kwargs)
            except self.client.exceptions.NoSuchBucket as exc:
                raise S3BucketInvalidError(
                    bucket=exc.response.get("Error", {}).get("BucketName", "undefined")
                ) from exc
            except botocore_exc.ClientError as exc:
                if exc.response.get("Error", {}).get("Code") == "404":
                    if exc.operation_name == "HeadObject":
                        raise S3KeyNotFoundError(bucket=args[0], key=args[1]) from exc
                    if exc.operation_name == "HeadBucket":
                        raise S3BucketInvalidError(bucket=args[0]) from exc
                if exc.response.get("Error", {}).get("Code") == "403":
                    if exc.operation_name == "HeadBucket":
                        raise S3BucketInvalidError(bucket=args[0]) from exc
                raise S3AccessError from exc
            except botocore_exc.EndpointConnectionError as exc:
                raise S3AccessError from exc

            except botocore_exc.BotoCoreError as exc:
                log.exception("Unexpected error in s3 client: ")
                raise S3AccessError from exc

            return response

        return wrapper

    return decorator


def update_task_progress(
    task_progress: TaskProgress | None,
    message: ProgressMessage | None = None,
    progress: ProgressPercent | None = None,
) -> None:
    logger.debug("%s [%s]", message or "", progress or "n/a")
    if task_progress:
        task_progress.update(message=message, percent=progress)


@dataclass
class S3TransferDataCB:
    task_progress: TaskProgress | None
    total_bytes_to_transfer: ByteSize
    task_progress_message_prefix: str = ""
    _total_bytes_copied: int = 0

    def __post_init__(self):
        self.copy_transfer_cb(0)

    def finalize_transfer(self):
        self.copy_transfer_cb(self.total_bytes_to_transfer - self._total_bytes_copied)

    def copy_transfer_cb(self, copied_bytes: int):
        self._total_bytes_copied += copied_bytes
        if self.total_bytes_to_transfer != 0:
            update_task_progress(
                self.task_progress,
                f"{self.task_progress_message_prefix} - "
                f"{parse_obj_as(ByteSize,self._total_bytes_copied).human_readable()}"
                f"/{self.total_bytes_to_transfer.human_readable()}]",
                self._total_bytes_copied / self.total_bytes_to_transfer,
            )
