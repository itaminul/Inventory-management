import logging

logger = logging.getLogger("inventory")


def debug(message: str):
    logger.debug(message)


def info(message: str):
    logger.info(message)


def warning(message: str):
    logger.warning(message)


def error(message: str):
    logger.error(message)


def exception(message: str):
    logger.exception(message)