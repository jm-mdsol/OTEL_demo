# Setup logging for the root logger, and Gunicorn
# This must come after the app is setup
import warnings
import astinus
import logging


def setup_logging(app_logger: logging.Logger = None):

    logging.basicConfig(level="INFO")

    if logging.root.level > logging.DEBUG:
        warnings.simplefilter(action="ignore", category=FutureWarning)

    # setup root logger
    root_logger: logging.Logger = astinus.Configurator.setup_logger_for(
       "otellogger", "1.0.0"
    )

    # setup gunicorn logger
    gunicorn_logger = astinus.Configurator.setup_logger_for(
        "otellogger", "1.0.0", "gunicorn.access"
    )

    if app_logger:
        # see: https://trstringer.com/logging-flask-gunicorn-the-manageable-way/ for why this is needed
        # in short, this makes flask use the gunicorn loggers and uses them as the source of truth
        # print("app_logger found")
        app_logger.handlers = gunicorn_logger.handlers
        app_logger.setLevel(gunicorn_logger.level)



