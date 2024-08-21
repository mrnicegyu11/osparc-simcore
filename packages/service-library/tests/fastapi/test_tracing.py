# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import os
from asyncio import AbstractEventLoop

import pytest
from fastapi import FastAPI
from pydantic import ValidationError
from servicelib.fastapi.tracing import (
    setup_opentelemtry_instrumentation,  # pylint: disable=no-name-in-module
)
from settings_library.tracing import TracingSettings

mock_app = FastAPI(title="Opentelemetry example")


@pytest.fixture
def tracing_settings_in(request):
    return request.param


@pytest.fixture()
def set_and_clean_settings_env_vars(tracing_settings_in):
    if tracing_settings_in[0]:
        os.environ["TRACING_OTEL_COLLECTOR_ENDPOINT"] = tracing_settings_in[0]
    if tracing_settings_in[1]:
        os.environ["TRACING_OTEL_COLLECTOR_PORT"] = str(tracing_settings_in[1])
    yield
    os.environ.pop("TRACING_OTEL_COLLECTOR_ENDPOINT", None)
    os.environ.pop("TRACING_OTEL_COLLECTOR_PORT", None)


@pytest.mark.parametrize(
    "tracing_settings_in",
    [
        ("http://otel-collector", 4318),
        ("http://otel-collector", "4318"),
    ],
    indirect=True,
)
def test_valid_tracing_settings(
    set_and_clean_settings_env_vars,
    event_loop: AbstractEventLoop,
    tracing_settings_in: TracingSettings,
):
    app = mock_app
    tracing_settings = TracingSettings()
    setup_opentelemtry_instrumentation(
        app,
        tracing_settings=tracing_settings,
        service_name="Mock-Openetlemetry-Pytest",
    )
    setup_opentelemtry_instrumentation(
        app,
        tracing_settings=tracing_settings,
        service_name="Mock-Openetlemetry-Pytest",
    )


@pytest.mark.parametrize(
    "tracing_settings_in",
    [
        ("http://otel-collector", 80),
        ("http://otel-collector", 1238712936),
        ("otel-collector", 4318),
        ("httsdasp://ot@##el-collector", 4318),
        (None, "1238712936"),
    ],
    indirect=True,
)
def test_invalid_tracing_settings(
    set_and_clean_settings_env_vars,
    event_loop: AbstractEventLoop,
    tracing_settings_in: TracingSettings,
):
    app = mock_app
    with pytest.raises((BaseException, ValidationError, TypeError)):  # noqa: PT012
        tracing_settings = TracingSettings()
        setup_opentelemtry_instrumentation(
            app,
            tracing_settings=tracing_settings,
            service_name="Mock-Openetlemetry-Pytest",
        )


@pytest.mark.parametrize(
    "tracing_settings_in",  # noqa: PT002
    [("", ""), ("", None), (None, None)],
    indirect=True,
)
def test_missing_tracing_settings(
    set_and_clean_settings_env_vars,
    event_loop: AbstractEventLoop,
    tracing_settings_in: TracingSettings,
):
    app = mock_app
    tracing_settings = TracingSettings()
    setup_opentelemtry_instrumentation(
        app,
        tracing_settings=tracing_settings,
        service_name="Mock-Openetlemetry-Pytest",
    )


@pytest.mark.parametrize(
    "tracing_settings_in",  # noqa: PT002
    [("http://otel-collector", None), (None, 4318)],
    indirect=True,
)
def test_incomplete_tracing_settings(
    set_and_clean_settings_env_vars,
    event_loop: AbstractEventLoop,
    tracing_settings_in: TracingSettings,
):
    pass
