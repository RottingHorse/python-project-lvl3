"""Web module."""
import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from page_loader.constants import (
    DASH,
    DIR_SUFFIX,
    DOT,
    HREF,
    HTML_SUFFIX,
    SLASH,
    SRC,
)
from page_loader.io import make_name, write_to_file
from page_loader.log import logger
from progress.bar import Bar

PROGRESS = 25


def _make_soup(url):
    response = _get_from_url(url)
    return BeautifulSoup(response.text, 'html.parser')


def _get_from_url(url):
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        logger.error(err)
    return response


def _is_same_domain(link_url, page_url):
    parsed_link = urlparse(link_url)
    parsed_page = urlparse(page_url)
    return parsed_link.netloc == parsed_page.netloc


def _generate_url(link, url):
    if 'jquery' in link:
        return None
    if not urlparse(link).scheme:
        return url + link
    if _is_same_domain(link, url):
        return link
    return None


def _make_file_name(res_path, tag, base_url):
    if tag.name == 'script':
        tail = urlparse(res_path).path.replace(SLASH, DASH)
    else:
        tail = res_path.replace(SLASH, DASH)
    res_path = make_name(base_url) + tail
    if tag.name == 'link' and DOT not in res_path:
        res_path += HTML_SUFFIX
    return res_path


def _download_resource(file_path: str, tag, base_url, attr):
    try:
        res_path = tag[attr]
    except KeyError:
        return
    res_url = _generate_url(res_path, base_url)
    if res_url is None:
        return
    progress_bar = Bar(res_url, max=100)

    res_resp = _get_from_url(res_url)
    progress_bar.next(PROGRESS)
    res_path = _make_file_name(res_path, tag, base_url)
    progress_bar.next(PROGRESS)
    full_path = os.path.join(res_path, file_path, res_path)
    if tag.name == 'img':
        write_to_file(full_path, res_resp.content, flag='wb')
    else:
        write_to_file(full_path, res_resp.text)
    progress_bar.next(PROGRESS)
    tag[attr] = os.path.join(make_name(base_url, DIR_SUFFIX), res_path)
    progress_bar.next(PROGRESS)
    progress_bar.finish()


def do_all_work(url: str, files_dir_path: str) -> str:
    """Do BeautifulSoup from URL, downloads all resources and writes to files.

    Also changes links to downloaded resources.

    Args:
        url (str): URL to download
        files_dir_path (str): Path to files directory

    Returns:
        str: Prettified HTML from BeautifulSoup
    """
    soup = _make_soup(url)
    for img in soup.find_all('img'):
        _download_resource(files_dir_path, img, url.strip(SLASH), SRC)

    for link in soup.find_all('link'):
        _download_resource(files_dir_path, link, url.strip(SLASH), HREF)

    for script in soup.find_all('script'):
        _download_resource(files_dir_path, script, url.strip(SLASH), SRC)
    return soup.prettify()
