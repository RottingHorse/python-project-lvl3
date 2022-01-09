"""Page loader."""
import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

HTML_SUFFIX = '.html'
DIR_SUFFIX = '_files'
SLASH = '/'
DOT = '.'
DASH = '-'


def _make_name(url: str, end: str = '') -> str:
    parsed_url = urlparse(url)

    return '{0}{1}{2}'.format(
        parsed_url.netloc.replace(DOT, DASH),
        parsed_url.path.replace(SLASH, DASH),
        end,
    )


def _make_paths(output, url):
    if output == 'current':
        output_html_path = os.path.join(
            os.getcwd(),
            _make_name(url, HTML_SUFFIX),
        )
        files_dir_path = os.path.join(os.getcwd(), _make_name(url, DIR_SUFFIX))
    else:
        output_html_path = os.path.join(output, _make_name(url, HTML_SUFFIX))
        files_dir_path = os.path.join(output, _make_name(url, DIR_SUFFIX))
    return files_dir_path, output_html_path


def _make_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def _download_image(files_dir_path: str, link, url):
    img_path = link['src']
    img_resp = requests.get(url + img_path)
    img_resp.raise_for_status()
    img_path = _make_name(url) + img_path.replace(SLASH, DASH)
    full_path = os.path.join(files_dir_path, img_path)
    with open(full_path, 'wb') as img_file:
        img_file.write(img_resp.content)
    link['src'] = os.path.join(_make_name(url, DIR_SUFFIX), img_path)


def download(url: str, output: str = 'current') -> str:
    """Do load web page and save to html file.

    Args:
        url (str): URL of requested web page.
        output (str): Path to directory to save.

    Returns:
        str: Path to saved file.
    """
    files_dir_path, output_html_path = _make_paths(output, url.strip(SLASH))

    if not os.path.exists(files_dir_path):
        os.makedirs(files_dir_path)

    soup = _make_soup(url)
    for link in soup.find_all('img'):
        _download_image(files_dir_path, link, url.strip(SLASH))

    with open(output_html_path, 'w') as out_file:
        out_file.write(soup.prettify())

    return output_html_path
