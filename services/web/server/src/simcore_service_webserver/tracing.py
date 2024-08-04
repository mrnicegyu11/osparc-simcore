import logging

from aiohttp import web
from servicelib.aiohttp.application_setup import ModuleCategory, app_module_setup
from servicelib.aiohttp.tracing import setup_tracing
from settings_library.tracing import UNDEFINED_CLIENT_NAME, TracingSettings

from ._constants import APP_SETTINGS_KEY

log = logging.getLogger(__name__)


def get_plugin_settings(app: web.Application) -> TracingSettings:
    settings = app[APP_SETTINGS_KEY].WEBSERVER_TRACING
    assert settings, "setup_settings not called?"  # nosec
    assert isinstance(settings, TracingSettings)  # nosec
    return settings


@app_module_setup(
    __name__, ModuleCategory.ADDON, settings_name="WEBSERVER_TRACING", logger=log
)
def setup_app_tracing(app: web.Application):
    settings: TracingSettings = get_plugin_settings(app)
    #

    service_name = settings.TRACING_CLIENT_NAME
    if service_name == UNDEFINED_CLIENT_NAME:
        service_name = "simcore_service_webserver"

    return setup_tracing(
        app,
        service_name=service_name,
        otel_collector_endpoint=settings.TRACING_OTEL_COLLECTOR_ENDPOINT,
        otel_collector_port=settings.TRACING_OTEL_COLLECTOR_PORT,
    )
