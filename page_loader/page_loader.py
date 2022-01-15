"""Page loader."""
import os
import logging
from logging import Formatter, StreamHandler
import sys
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


logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='%(message)s'))
logger.addHandler(handler)


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
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.error(e)
    return BeautifulSoup(response.text, 'html.parser')


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


def _download_image(files_dir_path: str, img, url):
    img_path = img[SRC]
    img_url = url + img_path
    img_resp = requests.get(img_url)
    try:
        img_resp.raise_for_status()
    except requests.HTTPError as e:
        logger.error(e)
    img_path = _make_name(url) + img_path.replace(SLASH, DASH)
    full_path = os.path.join(files_dir_path, img_path)
    try:
        with open(full_path, 'wb') as img_file:
            img_file.write(img_resp.content)
    except OSError:
        logger.error(f"Can't write to file {full_path}")
    img[SRC] = os.path.join(_make_name(url, DIR_SUFFIX), img_path)
    logger.warning(f'✔  {img_url}')


def _download_script(files_dir_path, script, url):
    try:
        script_src = script[SRC]
    except KeyError:
        return
    script_url = _generate_url(script_src, url)
    if script_url is None:
        return
    script_resp = requests.get(script_url)
    try:
        script_resp.raise_for_status()
    except requests.HTTPError as e:
        logger.error(e)
    scr_path = _make_name(url) + urlparse(script_src).path.replace(SLASH, DASH)
    full_path = os.path.join(files_dir_path, scr_path)
    try:
        with open(full_path, 'w') as script_file:
            script_file.write(script_resp.text)
    except OSError:
        logger.error(f"Can't write to file {full_path}")
    script[SRC] = os.path.join(_make_name(url, DIR_SUFFIX), scr_path)
    logger.warning(f'✔  {script_url}')


def _download_link(files_dir_path, link, url):
    link_href = link[HREF]
    link_url = _generate_url(link_href, url)
    if link_url is None:
        return
    link_resp = requests.get(link_url)
    try:
        link_resp.raise_for_status()
    except requests.HTTPError as e:
        logger.error(e)
    link_path = _make_name(url) + link_href.replace(SLASH, DASH)
    if DOT not in link_path:
        link_path += HTML_SUFFIX
    full_path = os.path.join(files_dir_path, link_path)
    try:
        with open(full_path, 'w') as link_file:
            link_file.write(link_resp.text)
    except OSError:
        logger.error(f"Can't write to file {full_path}")
    link[HREF] = os.path.join(_make_name(url, DIR_SUFFIX), link_path)
    logger.warning(f'✔  {link_url}')


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
        try:
            os.makedirs(files_dir_path)
        except OSError:
            logger.exception(f"Cant't create directory '{files_dir_path}'")

    soup = _make_soup(url)
    for img in soup.find_all('img'):
        _download_image(files_dir_path, img, url.strip(SLASH))

    for link in soup.find_all('link'):
        _download_link(files_dir_path, link, url.strip(SLASH))

    for script in soup.find_all('script'):
        _download_script(files_dir_path, script, url.strip(SLASH))
    try:
        with open(output_html_path, 'w') as out_file:
            out_file.write(soup.prettify())
    except OSError:
        logger.error(f"Can't write to file {output_html_path}")
    return output_html_path
