from opentelemetry import trace
import requests
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from fastapi.logger import logger

def send_requests():
    headers = {}
    TraceContextTextMapPropagator().inject(headers)
    logger.info(f"sending headers {headers}")
    return headers



# tracer = trace.get_tracer(__name__)


# def send_requests(url):
#     header = {}
#     TraceContextTextMapPropagator().inject(header)
#     res = requests.get(url, headers=header)
#     logger.info(f"header: {header}")

def get_headers(request, header_name, endpoint):
    headers = dict(request.headers)
    traceparent = request.headers.getlist(header_name)
    carrier = {"traceparent": traceparent[0]}
    parent_span_id = traceparent[0].split('-')[2]
    print("parent_span_id", parent_span_id)
    ctx = TraceContextTextMapPropagator().extract(carrier)
    # with tracer.start_as_current_span(f"/{endpoint}", context=ctx):
    logger.info("Trace context set successfully")

    return parent_span_id
