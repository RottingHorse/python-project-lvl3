"""IO module."""
import os
import sys
from urllib.parse import urlparse

from page_loader.constants import DASH, DIR_SUFFIX, DOT, HTML_SUFFIX, SLASH
from page_loader.log import logger

EXIT_CODE = 2


def create_dir(files_dir_path: str):
    """Do create directories for path.

    Args:
        files_dir_path (str): Path to create directories
    """
    if not os.path.exists(files_dir_path):
        try:
            os.makedirs(files_dir_path)
        except OSError:
            logger.error(f"Cant't create directory '{files_dir_path}'")
            sys.exit(EXIT_CODE)


def make_name(url: str, end: str = '') -> str:
    """Do make filename or directory name from URL, depends on end.

    Args:
        url (str): URL to make name
        end (str): Last few characters of name. Defaults to ''.

    Returns:
        str: Name of file or directory
    """
    parsed_url = urlparse(url)

    return '{0}{1}{2}'.format(
        parsed_url.netloc.replace(DOT, DASH),
        parsed_url.path.replace(SLASH, DASH),
        end,
    )


def make_paths(output: str, url: str):
    """Do make paths for output HTML file and directory for files.

    Args:
        output (str): Base output directory
        url (str): Web page URL

    Returns:
        tuple(str): Directory path, HTML file path
    """
    if output == 'current':
        output_html_path = os.path.join(
            os.getcwd(),
            make_name(url, HTML_SUFFIX),
        )
        files_dir_path = os.path.join(os.getcwd(), make_name(url, DIR_SUFFIX))
    else:
        output_html_path = os.path.join(output, make_name(url, HTML_SUFFIX))
        files_dir_path = os.path.join(output, make_name(url, DIR_SUFFIX))
    return files_dir_path, output_html_path


def write_to_file(file_path: str, web_content, flag: str = 'w'):
    """Do write text or image content to file.

    Args:
        file_path (str): Path to result file
        web_content (str | bytes): Content to write
        flag (str): Write flag, for image sets to 'wb'. Defaults to 'w'.
    """
    try:
        with open(file_path, flag) as out_file:
            out_file.write(web_content)
    except OSError:
        logger.error(f"Can't write to file {file_path}")
        sys.exit(EXIT_CODE)
