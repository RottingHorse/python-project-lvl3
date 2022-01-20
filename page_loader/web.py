"""Web module."""
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from page_loader.log import logger


def get_from_url(url: str) -> requests.Response:
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


def _make_soup(url: str) -> BeautifulSoup:
    raw_html = get_from_url(url)
    return BeautifulSoup(raw_html, 'html.parser')

def _parse_tag(tag: Tag, files_dir_path: str) -> tuple[str]:
    pass

def _write_new_src(tag: Tag, new_src: str):
    pass

def prepare(url: str, files_dir_path: str) -> tuple[str, tuple]:
    """Do download HTML file, find all tags with resources, changes resource tags with local sources.

    Args:
        url (str): URL to download
        files_dir_path (str): Path to local resources

    Returns:
        tuple[str, tuple]: Modified HTML file, tuple with resources URLs and pathes to save
    """
    soup = _make_soup(url)
    resources = []
    res_tags = soup.find_all(["img", "link", "script"])
    for tag in res_tags:
        res_url, file_path, new_src = _parse_tag(tag, files_dir_path)
        _write_new_src(tag, new_src)
        resources.append(res_url, file_path)


    html_file = soup.prettify()
    return html_file, resources

