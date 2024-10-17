import sys
from loguru import logger

logger.remove()

logger.add(
    sink=sys.stdout,
    format=(
        "<yellow><b>[HEATING]</b></yellow> "
        "| <white>{time:HH:mm:ss}</white> "
        "| <level>{level: <8}</level> "
        "| <white><b>{message}</b></white>"
    ),
    colorize=True
)

logger = logger.opt(colors=True)

def info(text):
    return logger.info(text)


def debug(text):
    return logger.debug(text)


def warning(text):
    return logger.warning(text)


def error(text):
    return logger.error(text)


def critical(text):
    return logger.critical(text)


def success(text):
    return logger.success(text)