import logging

from pythonjsonlogger.json import JsonFormatter


def setup_logging() -> None:
    """Configure structured JSON logging for the application."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
