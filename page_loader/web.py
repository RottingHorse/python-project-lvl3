"""Web module."""
import requests
from bs4 import BeautifulSoup

from page_loader.log import logger


def make_soup(url: str)-> BeautifulSoup:
    """Do make BeautifulSoup from URL

    Args:
        url (str): Web page URL

    Returns:
        BeautifulSoup: BeautifulSoup from URL
    """
    response = get_from_url(url)
    logger.info('BeautifulSoup was created')
    return BeautifulSoup(response.text, 'html.parser')


def get_from_url(url: str) -> requests.Response:
    """Do download any resource from URL

    Args:
        url (str): URL to download

    Returns:
        requests.Response: Downloaded response object
    """
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f'Resource from {url} was downloaded')
    return response
