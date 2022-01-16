"""Page loader main module."""
from asyncio.log import logger
import os

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

from page_loader.constants import ATTRIBUTES, DIR_SUFFIX, SLASH
from page_loader.io import create_dir, write_to_file
from page_loader.names import generate_url, make_file_name, make_paths, make_name
from page_loader.web import get_from_url, make_soup


def _get_resource(file_path: str, tag: Tag, base_url, attr):
    try:
        res_path = tag[attr]
    except KeyError:
        return
    res_url = generate_url(res_path, base_url)
    if res_url is None:
        return
    try:
        res_content = get_from_url(res_url)
    except requests.RequestException as err:
        logger.info(err)
        logger.warning(f'Unable to download {res_url}')
    res_path = make_file_name(res_path, tag, base_url)
    full_path = os.path.join(res_path, file_path, res_path)
    new_src = os.path.join(make_name(base_url, DIR_SUFFIX), res_path)
    tag[attr] = new_src
    return res_content, full_path


def _get_tag(tag_name: str, soup: BeautifulSoup, files_dir_path: str, url: str):
    attr_name = ATTRIBUTES[tag_name]
    tags = []
    for tag in soup.find_all(tag_name):
        payload = _get_resource(files_dir_path, tag,
                                url, attr_name)
        tags.append(payload)
    return tags


def download(url: str, output: str = 'current') -> str:
    """Do load web page and save to html file.

    Args:
        url (str): URL of requested web page.
        output (str): Path to directory to save.

    Returns:
        str: Path to saved file.
    """
    url = url.strip(SLASH)
    files_dir_path, output_html_path = make_paths(output, url)

    soup = make_soup(url)

    tags_content = []

    tags_content.extend(_get_tag('img', soup, files_dir_path, url))
    tags_content.extend(_get_tag('link', soup, files_dir_path, url))
    tags_content.extend(_get_tag('script', soup, files_dir_path, url))

    html_file = soup.prettify()

    create_dir(files_dir_path)

    for tag in tags_content:
        content_to_write, full_path = tag
        try:
            write_to_file(full_path, content_to_write)
        except OSError as err:
            logger.info(err)
            logger.warning(f"Can't write file {full_path}")
    try:
        write_to_file(output_html_path, html_file)
    except OSError as err:
        logger.info(err)
        logger.warning(f"Can't write file {output_html_path}")
    return output_html_path
