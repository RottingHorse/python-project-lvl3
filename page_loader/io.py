"""IO module."""
import os
from urllib.parse import urlparse

from page_loader.constants import DASH, DIR_SUFFIX, DOT, HTML_SUFFIX, SLASH
from page_loader.log import logger


def create_dir(files_dir_path: str):
    """Do create directories for path.

    Args:
        files_dir_path (str): Path to create directories
    """
    if not os.path.exists(files_dir_path):
        os.makedirs(files_dir_path)
        logger.info(f'Created directory {files_dir_path}')


def write_to_file(file_path: str, web_content, flag: str = 'w'):
    """Do write text or image content to file.

    Args:
        file_path (str): Path to result file
        web_content (str | bytes): Content to write
        flag (str): Write flag, for image sets to 'wb'. Defaults to 'w'.
    """
    with open(file_path, flag) as out_file:
        out_file.write(web_content)
        logger.info(f'Content was written to file {file_path}')
