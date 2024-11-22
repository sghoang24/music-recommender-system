# pylint: disable=E0401
"""Root constant define."""

import os

from dotenv import load_dotenv

load_dotenv()

APP_HOST = os.getenv("APP_HOST")
APP_PORT = os.getenv("APP_PORT")
