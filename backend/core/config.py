# pylint: disable=E0401
"""Define config for project."""

from __future__ import annotations

import logging
import sys
import os
import json
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

PROJECT_NAME: str = config("Music Recommender System", default="Music Recommender System")
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


GENRES_MAP = {
    "Pop": "pop",
    "Rock": "rock",
    "Hip-Hop": "hiphop",
    "Electronic": "electronic",
    "Jazz": "jazz",
    "Country": "country",
    "Classical": "classical",
    "Instrumental": "instrumental",
}

file_path = "./data/map_track_ids.json"

# Check if the file exists
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        map_track_ids = json.load(f)
    MAX_IDS_EXIST = True
else:
    print(f"File {file_path} does not exist.")
    MAX_IDS_EXIST = False
