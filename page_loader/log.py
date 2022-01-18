"""Logging module."""
import logging

FORMAT = "\n%(message)s"
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logger = logging.getLogger()
