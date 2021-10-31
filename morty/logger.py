import logging

LOG_LEVEL = logging.INFO
DEFAULT_LOG_MESSAGE = "%(asctime)s %(levelname) -7s " "%(name)s: %(message)s"

logger = logging.getLogger(__name__)

logger.setLevel(LOG_LEVEL)
logger.propagate = False

console_handler = logging.StreamHandler()
formatter = logging.Formatter(fmt=DEFAULT_LOG_MESSAGE)
formatter.default_msec_format = "%s.%03d"
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

__all__ = ("logger",)
