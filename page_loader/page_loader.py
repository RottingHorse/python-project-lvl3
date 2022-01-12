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
SRC = 'src'
HREF = 'href'


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


def _download_image(files_dir_path: str, img, url):
    img_path = img[SRC]
    img_resp = requests.get(url + img_path)
    img_resp.raise_for_status()
    img_path = _make_name(url) + img_path.replace(SLASH, DASH)
    full_path = os.path.join(files_dir_path, img_path)
    with open(full_path, 'wb') as img_file:
        img_file.write(img_resp.content)
    img[SRC] = os.path.join(_make_name(url, DIR_SUFFIX), img_path)


def _is_same_domain(link_url, page_url):
    parsed_link = urlparse(link_url)
    parsed_page = urlparse(page_url)
    return parsed_link.netloc == parsed_page.netloc


def _generate_url(link, url):
    if not urlparse(link).scheme:
        return url + link
    if _is_same_domain(link, url):
        return link
    return None


def _download_script(files_dir_path, script, url):
    script_src = script[SRC]
    script_url = _generate_url(script_src, url)
    if script_url is None:
        return
    script_resp = requests.get(script_url)
    script_resp.raise_for_status()
    scr_path = _make_name(url) + urlparse(script_src).path.replace(SLASH, DASH)
    full_path = os.path.join(files_dir_path, scr_path)
    with open(full_path, 'w') as script_file:
        script_file.write(script_resp.text)
    script[SRC] = os.path.join(_make_name(url, DIR_SUFFIX), scr_path)


def _download_link(files_dir_path, link, url):
    link_href = link[HREF]
    link_url = _generate_url(link_href, url)
    if link_url is None:
        return
    link_resp = requests.get(link_url)
    link_resp.raise_for_status()
    link_path = _make_name(url) + link_href.replace(SLASH, DASH)
    if DOT not in link_path:
        link_path += HTML_SUFFIX
    full_path = os.path.join(files_dir_path, link_path)
    with open(full_path, 'w') as link_file:
        link_file.write(link_resp.text)
    link[HREF] = os.path.join(_make_name(url, DIR_SUFFIX), link_path)


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
    for img in soup.find_all('img'):
        _download_image(files_dir_path, img, url.strip(SLASH))

    for link in soup.find_all('link'):
        _download_link(files_dir_path, link, url.strip(SLASH))

    for script in soup.find_all('script'):
        _download_script(files_dir_path, script, url.strip(SLASH))

    with open(output_html_path, 'w') as out_file:
        out_file.write(soup.prettify())

    return output_html_path
