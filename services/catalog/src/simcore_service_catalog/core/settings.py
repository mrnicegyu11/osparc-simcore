import logging
from functools import cached_property
from typing import Annotated, Final

from models_library.api_schemas_catalog.services_specifications import (
    ServiceSpecifications,
)
from models_library.basic_types import LogLevel
from models_library.services_resources import ResourcesDict, ResourceValue
from pydantic import (
    AliasChoices,
    ByteSize,
    Field,
    NonNegativeInt,
    PositiveInt,
    TypeAdapter,
)
from servicelib.logging_utils_filtering import LoggerName, MessageSubstring
from settings_library.application import BaseApplicationSettings
from settings_library.base import BaseCustomSettings
from settings_library.http_client_request import ClientRequestSettings
from settings_library.postgres import PostgresSettings
from settings_library.rabbit import RabbitSettings
from settings_library.tracing import TracingSettings
from settings_library.utils_logging import MixinLoggingSettings

_logger = logging.getLogger(__name__)


class DirectorSettings(BaseCustomSettings):
    DIRECTOR_HOST: str
    DIRECTOR_PORT: int = 8080
    DIRECTOR_VTAG: str = "v0"

    @cached_property
    def base_url(self) -> str:
        return f"http://{self.DIRECTOR_HOST}:{self.DIRECTOR_PORT}/{self.DIRECTOR_VTAG}"


_in_bytes = TypeAdapter(ByteSize).validate_python

_DEFAULT_RESOURCES: Final[ResourcesDict] = ResourcesDict(
    CPU=ResourceValue(limit=0.1, reservation=0.1),
    RAM=ResourceValue(limit=_in_bytes("2Gib"), reservation=_in_bytes("2Gib")),
)


_DEFAULT_SERVICE_SPECIFICATIONS: Final[
    ServiceSpecifications
] = ServiceSpecifications.model_validate({})


class ApplicationSettings(BaseApplicationSettings, MixinLoggingSettings):
    LOG_LEVEL: Annotated[
        LogLevel,
        Field(
            validation_alias=AliasChoices(
                "CATALOG_LOG_LEVEL", "CATALOG_LOGLEVEL", "LOG_LEVEL", "LOGLEVEL"
            ),
        ),
    ] = LogLevel.INFO
    CATALOG_LOG_FORMAT_LOCAL_DEV_ENABLED: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "CATALOG_LOG_FORMAT_LOCAL_DEV_ENABLED", "LOG_FORMAT_LOCAL_DEV_ENABLED"
        ),
        description="Enables local development log format. WARNING: make sure it is disabled if you want to have structured logs!",
    )
    CATALOG_LOG_FILTER_MAPPING: dict[LoggerName, list[MessageSubstring]] = Field(
        default_factory=dict,
        validation_alias=AliasChoices(
            "CATALOG_LOG_FILTER_MAPPING", "LOG_FILTER_MAPPING"
        ),
        description="is a dictionary that maps specific loggers (such as 'uvicorn.access' or 'gunicorn.access') to a list of log message patterns that should be filtered out.",
    )
    CATALOG_DEV_FEATURES_ENABLED: bool = Field(
        default=False,
        description="Enables development features. WARNING: make sure it is disabled in production .env file!",
    )

    CATALOG_POSTGRES: PostgresSettings | None = Field(
        json_schema_extra={"auto_default_from_env": True}
    )

    CATALOG_RABBITMQ: RabbitSettings = Field(
        json_schema_extra={"auto_default_from_env": True}
    )

    CATALOG_CLIENT_REQUEST: ClientRequestSettings | None = Field(
        json_schema_extra={"auto_default_from_env": True}
    )

    CATALOG_DIRECTOR: DirectorSettings | None = Field(
        json_schema_extra={"auto_default_from_env": True}
    )

    CATALOG_PROMETHEUS_INSTRUMENTATION_ENABLED: bool = True

    CATALOG_PROFILING: bool = False

    # BACKGROUND TASK
    CATALOG_BACKGROUND_TASK_REST_TIME: PositiveInt = 60
    CATALOG_BACKGROUND_TASK_WAIT_AFTER_FAILURE: PositiveInt = 5  # secs

    CATALOG_SERVICES_DEFAULT_RESOURCES: ResourcesDict = _DEFAULT_RESOURCES
    CATALOG_SERVICES_DEFAULT_SPECIFICATIONS: ServiceSpecifications = (
        _DEFAULT_SERVICE_SPECIFICATIONS
    )
    CATALOG_TRACING: TracingSettings | None = Field(
        json_schema_extra={"auto_default_from_env": True},
        description="settings for opentelemetry tracing",
    )

    DIRECTOR_DEFAULT_MAX_MEMORY: NonNegativeInt = Field(default=0)
    DIRECTOR_DEFAULT_MAX_NANO_CPUS: NonNegativeInt = Field(default=0)
