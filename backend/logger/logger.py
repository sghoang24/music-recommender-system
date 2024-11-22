"""Logger."""

import logging
import os
from datetime import datetime

from core.config import LOGGING_LEVEL


class UvicornFormatter(logging.Formatter):
    """Uvicorn Formatter."""

    FORMAT = (
        "\033[38;5;244m%(asctime)s\033[0m"
        " | "
        "%(levelname)-7s"
        " | "
        "\033[38;5;214m%(name)s\033[0m"
        " : "
        "\033[38;5;111m%(message)s\033[0m"
    )

    LEVEL_COLORS = {
        "DEBUG": "\033[38;5;32m",
        "INFO": "\033[38;5;36m",
        "WARNING": "\033[38;5;221m",
        "ERROR": "\033[38;5;196m",
        "CRITICAL": "\033[48;5;196;38;5;231m",
    }

    def format(self, record):
        """Config format"""
        levelname = record.levelname
        level_color = self.LEVEL_COLORS.get(levelname, "")
        record.levelname = f"{level_color}{levelname}\033[0m"
        record.asctime = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")
        return super().format(record)


class CustomLogger:
    """Logger Singleton Class."""

    _instance = None

    @classmethod
    def get_instance(cls):
        """Get the single instance of the logger."""
        if cls._instance is None:
            cls._instance = cls._configure_logging()
        return cls._instance

    @staticmethod
    def _configure_logging():
        """Initialize logging defaults for Project.

        This function does:
        - Assign INFO and DEBUG level to logger file handler and console handler.

        Returns:
            Logger.
        """
        logger = logging.getLogger()
        logger.setLevel(LOGGING_LEVEL)

        # Create a file handler with a lower log level
        current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        log_dir = os.path.join(current_dir, "logs", "backend")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "backend.log")
        print(f"-> Log file path: {log_file}")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(LOGGING_LEVEL)

        # Create a console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOGGING_LEVEL)

        # Create a formatter and add it to the handlers
        default_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s",
            "%d/%m/%Y %H:%M:%S",
        )

        file_handler.setFormatter(default_formatter)
        console_handler.setFormatter(UvicornFormatter(UvicornFormatter.FORMAT))

        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


custom_logger = CustomLogger.get_instance()
