import uvicorn
from fastapi import FastAPI, Request
from fastapi.logger import logger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from context_propgation_trial2.otel_settings.logging import setup_logging
from context_propgation_trial2.otel_settings.otel import setup_otel


app = FastAPI()
setup_logging(logger)
setup_otel("api")
FastAPIInstrumentor.instrument_app(app, excluded_urls=r"//[^/]*/$,/app_status")


@app.middleware("http")
async def get_parent_id(request: Request, call_next):

    parent_id = request.headers['traceparent'].split('-')[2]

    logger.info(f"reached middle ware and getting parent_span id")

    request.state.parent_id = parent_id
    response = await call_next(request)
    return response


@app.get("/create")
def create(request: Request):
   # logger.info(f"create endpoint ran successfully. parent_span_id  {request.state.parent_id }")
    logger.info('Log message', extra={'parent_span_id': request.state.parent_id})
    return {"success"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9094)
