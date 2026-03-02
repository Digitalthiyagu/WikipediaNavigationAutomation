"""
logger.py

Central logging configuration.
Used across framework.

Best Practice:
Never use print() in real frameworks.
Use logging module instead.
"""

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a logger instance.
    """

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("logs/test_execution.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger