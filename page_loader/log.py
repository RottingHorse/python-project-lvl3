"""Logging module."""
import logging


def setup_log():
    """Do setup logging."""
    fmt = "\n%(message)s"
    logging.basicConfig(level=logging.WARNING, format=fmt)
