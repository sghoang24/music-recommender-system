# pylint: disable=E0401
"""Define config for project."""

from __future__ import annotations

import json
import logging
import sys

import numpy as np
from core.logging import InterceptHandler
from dotenv import load_dotenv
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

load_dotenv()

API_PREFIX = "/api"

VERSION = "0.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

PROJECT_NAME: str = config("Recommendation Service", default="Recommendation Service")
ALLOWED_HOSTS: list[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# Logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

TOP_K = 5

embeded_images = np.load("./data/embeded_images.npy")
labels = np.load("./data/labels.npy")
with open("./data/embedd_metadata.json", "r", encoding="utf-8") as f:
    embedd_metadata = json.load(f)
