"""Web module."""
import os

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from page_loader.constants import ATTRIBUTES, DIR_SUFFIX
from page_loader.log import logger
from page_loader.names import generate_url, make_file_name, make_name


def get_from_url(url: str) -> requests.Response:
    """Do download any resource from URL.

    Args:
        url (str): URL to download

    Returns:
        requests.Response: Downloaded content
    """
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f"Resource from {url} was downloaded")
    return response.content


def _make_soup(url: str) -> BeautifulSoup:
    raw_html = get_from_url(url)
    return BeautifulSoup(raw_html, "html.parser")


def _parse_tag(tag: Tag, files_dir_path: str, url: str) -> tuple[str]:
    attr = ATTRIBUTES[tag.name]
    try:
        res_path = tag[attr]
    except KeyError:
        return None, None, None
    res_url = generate_url(res_path, url)
    if not res_url:
        return None, None, None
    res_path = make_file_name(res_path, tag, url)
    file_path = os.path.join(res_path, files_dir_path, res_path)
    new_src = os.path.join(make_name(url, DIR_SUFFIX), res_path)
    return res_url, file_path, new_src


def _write_new_src(tag: Tag, new_src: str):
    attr = ATTRIBUTES[tag.name]
    tag[attr] = new_src


def prepare(url: str, files_dir_path: str) -> tuple[str, tuple]:
    """Do download HTML file, find all tags with resources,
    changes resource tags with local sources.

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
        res_url, file_path, new_src = _parse_tag(tag, files_dir_path, url)
        if new_src:
            _write_new_src(tag, new_src)
        if res_url and file_path:
            resources.append((res_url, file_path))

    html_file = soup.prettify()
    return html_file, resources
