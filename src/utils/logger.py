"""Logging helpers."""
from __future__ import annotations

import logging
from logging import Logger

from .config import Settings


def get_logger(name: str, settings: Settings) -> Logger:
    """Configure and return a logger using provided settings."""

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(settings.log_level.upper())
    return logger
