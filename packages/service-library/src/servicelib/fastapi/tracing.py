""" Adds fastapi middleware for tracing using opentelemetry instrumentation.

"""

import logging

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterHTTP,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from settings_library.tracing import TracingSettings

log = logging.getLogger(__name__)
#########
try:
    from opentelemetry.instrumentation.aiopg import AsyncPGInstrumentor

    HAS_ASYNCPG = True
except ImportError:
    HAS_ASYNCPG = False
#########
try:
    from opentelemetry.instrumentation.asyncpg import AiopgInstrumentor

    HAS_AIPPG = True
except ImportError:
    HAS_AIPPG = False
#########
try:
    from opentelemetry.instrumentation.redis import RedisInstrumentor

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False
try:
    from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

    HAS_BOTOCORE = True
except ImportError:
    HAS_BOTOCORE = False


def setup_tracing(
    app: FastAPI, tracing_settings: TracingSettings, service_name: str
) -> None:
    if (
        not tracing_settings.TRACING_OPENTELEMETRY_COLLECTOR_ENDPOINT
        and not tracing_settings.TRACING_OPENTELEMETRY_COLLECTOR_PORT
    ):
        log.warning("Skipping opentelemetry tracing setup")
        return

    # Set up the tracer provider
    resource = Resource(attributes={"service.name": service_name})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    global_tracer_provider = trace.get_tracer_provider()
    assert isinstance(global_tracer_provider, TracerProvider)  # nosec
    tracing_destination: str = f"{tracing_settings.TRACING_OPENTELEMETRY_COLLECTOR_ENDPOINT}:{tracing_settings.TRACING_OPENTELEMETRY_COLLECTOR_PORT}/v1/traces"
    log.info(
        "Trying to connect service %s to opentelemetry tracing collector at %s.",
        service_name,
        tracing_destination,
    )
    # Configure OTLP exporter to send spans to the collector
    otlp_exporter = OTLPSpanExporterHTTP(endpoint=tracing_destination)
    span_processor = BatchSpanProcessor(otlp_exporter)
    global_tracer_provider.add_span_processor(span_processor)
    # Instrument FastAPI
    FastAPIInstrumentor().instrument_app(app)

    if HAS_AIPPG:
        log.info("Attempting to add aiopg opentelemetry autoinstrumentation...")
        AiopgInstrumentor().instrument()
    if HAS_ASYNCPG:
        log.info("Attempting to add asyncpg opentelemetry autoinstrumentation...")
        AsyncPGInstrumentor().instrument()
    if HAS_REDIS:
        log.info("Attempting to add redis opentelemetry autoinstrumentation...")
        RedisInstrumentor().instrument()
    if HAS_BOTOCORE:
        log.info("Attempting to add botocore opentelemetry autoinstrumentation...")
        BotocoreInstrumentor().instrument()
