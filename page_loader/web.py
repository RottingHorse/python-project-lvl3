"""Web module."""
import requests
from bs4 import BeautifulSoup
from page_loader.log import logger


def _make_soup(url: str) -> BeautifulSoup:
    """Do make BeautifulSoup from URL.

    Args:
        url (str): Web page URL

    Returns:
        BeautifulSoup: BeautifulSoup from URL
    """
    raw_html = _get_from_url(url)
    logger.info('BeautifulSoup was created')
    return BeautifulSoup(raw_html, 'html.parser')


def _get_from_url(url: str) -> requests.Response:
    """Do download any resource from URL.

    Args:
        url (str): URL to download

    Returns:
        requests.Response: Downloaded content
    """
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f'Resource from {url} was downloaded')
    return response.content

def prepare(url: str, files_dir_path: str):
    resources = []
    html_file = ""
    return html_file, resources
