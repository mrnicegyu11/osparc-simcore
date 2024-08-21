import logging
from collections.abc import Callable, Coroutine, Mapping
from contextlib import contextmanager
from functools import wraps
from inspect import signature
from typing import Any, Concatenate, NamedTuple, ParamSpec, TypeAlias, TypeVar

import httpx
from fastapi import HTTPException, status
from pydantic import ValidationError
from simcore_service_api_server.exceptions.backend_errors import BaseBackEndError

from ..models.schemas.errors import ErrorGet

_logger = logging.getLogger(__name__)

MSG_INTERNAL_ERROR_USER_FRIENDLY_TEMPLATE = "Oops! Something went wrong, but we've noted it down and we'll sort it out ASAP. Thanks for your patience! [{}]"

DEFAULT_BACKEND_SERVICE_STATUS_CODES: dict[int | str, dict[str, Any]] = {
    status.HTTP_429_TOO_MANY_REQUESTS: {
        "description": "Too many requests",
        "model": ErrorGet,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "model": ErrorGet,
    },
    status.HTTP_502_BAD_GATEWAY: {
        "description": "Unexpected error when communicating with backend service",
        "model": ErrorGet,
    },
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "description": "Service unavailable",
        "model": ErrorGet,
    },
    status.HTTP_504_GATEWAY_TIMEOUT: {
        "description": "Request to a backend service timed out.",
        "model": ErrorGet,
    },
}


ServiceHTTPStatus: TypeAlias = int
ApiHTTPStatus: TypeAlias = int


class ToApiTuple(NamedTuple):
    status_code: ApiHTTPStatus
    detail: Callable[[Any], str] | str | None = None


# service to public-api status maps
E = TypeVar("E", bound=BaseBackEndError)
HttpStatusMap: TypeAlias = Mapping[ServiceHTTPStatus, E]


def _get_http_exception_kwargs(
    service_name: str,
    service_error: httpx.HTTPStatusError,
    http_status_map: HttpStatusMap,
    **exception_ctx: Any,
):
    detail: str = ""
    headers: dict[str, str] = {}

    if exception_type := http_status_map.get(service_error.response.status_code):
        raise exception_type(**exception_ctx)

    if service_error.response.status_code in {
        status.HTTP_429_TOO_MANY_REQUESTS,
        status.HTTP_503_SERVICE_UNAVAILABLE,
        status.HTTP_504_GATEWAY_TIMEOUT,
    }:
        status_code = service_error.response.status_code
        detail = f"The {service_name} service was unavailable."
        if retry_after := service_error.response.headers.get("Retry-After"):
            headers["Retry-After"] = retry_after
    else:
        status_code = status.HTTP_502_BAD_GATEWAY
        detail = f"Received unexpected response from {service_name}"

    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        _logger.exception(
            "Converted status code %s from %s service to status code %s",
            f"{service_error.response.status_code}",
            service_name,
            f"{status_code}",
        )
    return status_code, detail, headers


Self = TypeVar("Self")
P = ParamSpec("P")
R = TypeVar("R")


@contextmanager
def service_exception_handler(
    service_name: str,
    http_status_map: HttpStatusMap,
    **context,
):
    status_code: int
    detail: str
    headers: dict[str, str] = {}

    try:

        yield

    except ValidationError as exc:
        detail = f"{service_name} service returned invalid response"
        _logger.exception(
            "Invalid data exchanged with %s service. %s", service_name, detail
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=detail, headers=headers
        ) from exc

    except httpx.HTTPStatusError as exc:

        status_code, detail, headers = _get_http_exception_kwargs(
            service_name, exc, http_status_map=http_status_map, **context
        )
        raise HTTPException(
            status_code=status_code, detail=detail, headers=headers
        ) from exc


def service_exception_mapper(
    service_name: str,
    http_status_map: HttpStatusMap,
) -> Callable[
    [Callable[Concatenate[Self, P], Coroutine[Any, Any, R]]],
    Callable[Concatenate[Self, P], Coroutine[Any, Any, R]],
]:
    def _decorator(member_func: Callable[Concatenate[Self, P], Coroutine[Any, Any, R]]):
        _assert_correct_kwargs(func=member_func, status_map=http_status_map)

        @wraps(member_func)
        async def _wrapper(self: Self, *args: P.args, **kwargs: P.kwargs) -> R:
            with service_exception_handler(service_name, http_status_map, **kwargs):
                return await member_func(self, *args, **kwargs)

        return _wrapper

    return _decorator


def _assert_correct_kwargs(func: Callable, status_map: HttpStatusMap):
    _required_kwargs = {
        name
        for name, param in signature(func).parameters.items()
        if param.kind == param.KEYWORD_ONLY
    }
    for exc_type in status_map.values():
        _exception_inputs = exc_type.named_fields()
        assert _exception_inputs.issubset(
            _required_kwargs
        ), f"{_exception_inputs - _required_kwargs} are inputs to `{exc_type.__name__}.msg_template` but not a kwarg in the decorated coroutine `{func.__module__}.{func.__name__}`"  # nosec
