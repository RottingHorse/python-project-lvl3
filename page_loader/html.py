"""Web module."""
import os

from bs4 import BeautifulSoup
from page_loader import url
from page_loader.constants import ATTRIBUTES, DIR_SUFFIX


def _make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _prepare_resources(files_dir_path, res_tags, base_url):
    resources = []
    for tag in res_tags:
        attr = ATTRIBUTES[tag.name]
        res_path = tag.get(attr, default=None)
        if not res_path:
            continue
        res_url = url.to_url(res_path, base_url)
        if not res_url:
            continue
        res_path = url.to_file_name(res_path, tag, base_url)
        file_path = os.path.join(res_path, files_dir_path, res_path)
        new_src = os.path.join(
            url.to_file_or_dir(base_url, DIR_SUFFIX),
            res_path,
        )
        if new_src:
            attr = ATTRIBUTES[tag.name]
            tag[attr] = new_src
        if res_url and file_path:
            resources.append((res_url, file_path))
    return resources


def prepare(raw_html: str, files_dir_path: str, base_url: str) -> tuple:
    """
    Do prepare HTML file.

    Changes resource tags with local sources.

    Args:
        raw_html (str): HTML to prepare
        files_dir_path (str): Path to local resources
        base_url (str): URL to generate links

    Returns:
        tuple: Modified HTML file, tuple with resources URLs and path's to save
    """
    soup = _make_soup(raw_html)

    res_tags = soup.find_all(["img", "link", "script"])
    resources = _prepare_resources(files_dir_path, res_tags, base_url)

    html_file = soup.prettify()
    return html_file, resources
