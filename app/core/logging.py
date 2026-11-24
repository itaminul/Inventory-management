import logging
import os

from logging.handlers import RotatingFileHandler

from app.core.config import settings


def setup_logging():

    log_level = getattr(
        logging,
        settings.LOG_LEVEL.upper(),
        logging.INFO
    )

    handlers = [logging.StreamHandler()]

    if settings.LOG_TO_FILE:

        log_directory = os.path.dirname(settings.LOG_FILE)

        if log_directory:
            os.makedirs(log_directory, exist_ok=True)

        file_handler = RotatingFileHandler(
            settings.LOG_FILE,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )

        handlers.append(file_handler)

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=handlers,
        force=True
    )