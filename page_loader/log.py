"""Logging module."""
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
messages_handler = logging.StreamHandler(stream=sys.stdout)
messages_handler.setLevel(logging.WARNING)
messages_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
logger.addHandler(messages_handler)
