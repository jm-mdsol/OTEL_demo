from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from opentelemetry.instrumentation.propagators import (
    TraceResponsePropagator,
    set_global_response_propagator,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def setup_otel(sub_component: str):
    sampler = ParentBasedTraceIdRatio(1.0)
    resource = Resource.create(
        {
            "service.name": "otellogger",
            "service.namespace": "component/sandbox",
            "application": "otellogger",
            "deployment.environment": "sandbox",
            "service.version": "1.0.0",
        }
    )
    tracer_provider = TracerProvider(sampler, resource)
    tracer_provider.add_span_processor \
        (BatchSpanProcessor(OTLPSpanExporter("https://tracing-grpc-sandbox.imedidata.net")))
    trace.set_tracer_provider(tracer_provider)
    set_global_response_propagator(TraceResponsePropagator())
    LoggingInstrumentor().instrument()
