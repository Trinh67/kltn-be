from app.helper.db import db_engine
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from setting import setting
from typing import Optional


def init_tracer(service_name: str, db_profiling: bool = False) -> Optional[Tracer]:
    if not setting.JAEGER_ENABLED:
        return None

    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: service_name})
        )
    )
    jaeger_exporter = JaegerExporter(
        agent_host_name=setting.JAEGER_AGENT_HOST, agent_port=setting.JAEGER_AGENT_PORT,
    )
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    if db_profiling:
        SQLAlchemyInstrumentor().instrument(engine=db_engine)

    RequestsInstrumentor().instrument()
    tracer = trace.get_tracer('send notification')
    return tracer
