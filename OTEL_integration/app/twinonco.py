import uvicorn
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi.logger import logger
from context_propgation_trial2.otel_settings.logging import setup_logging
from context_propgation_trial2.otel_settings.otel import setup_otel
from context_propgation_trial2.trace_settings.context_propagation import send_requests
import requests

app = FastAPI()
setup_logging(logger)
setup_otel("api")
FastAPIInstrumentor.instrument_app(app, excluded_urls=r"//[^/]*/$,/app_status")


@app.get("/apply_lda")
def call_state_manager():
    logger.info(f"calling state manager")
    res = requests.get("http://0.0.0.0:9094/create", headers=send_requests())
    return {"traces generated successfully"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9093)

#
# tracking_id = {'traceparent': '00-74dd941999961b27b28f65315367843c-2d872c8d64423496-01'}
#
# desired_value = tracking_id['traceparent'].split('-')[1]
#
# print(desired_value)