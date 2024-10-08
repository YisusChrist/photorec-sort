"""Logging configuration."""

import logging

from core_helpers.logs import setup_logger

from .consts import DEBUG, LOG_FILE, PACKAGE

# Create a logger instance
logger: logging.Logger = setup_logger(package=PACKAGE, log_file=LOG_FILE, debug=DEBUG)
