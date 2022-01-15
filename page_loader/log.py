"""Logging module."""
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
messages_handler = logging.StreamHandler()
messages_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
logger.addHandler(messages_handler)
