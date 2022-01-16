"""Page loader main module."""
import os

from page_loader.constants import DIR_SUFFIX, HREF, SLASH, SRC
from page_loader.io import create_dir, write_to_file
from page_loader.names import generate_url, make_file_name, make_paths, make_name
from page_loader.web import get_from_url, make_soup


def _download_resource(file_path: str, tag, base_url, attr):
    try:
        res_path = tag[attr]
    except KeyError:
        return
    res_url = generate_url(res_path, base_url)
    if res_url is None:
        return
    progress_bar = Bar(res_url, max=100)

    res_resp = get_from_url(res_url)
    progress_bar.next(PROGRESS)
    res_path = make_file_name(res_path, tag, base_url)
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

    soup = make_soup(url)
    if soup:
        create_dir(files_dir_path)

    for img in soup.find_all('img'):
        _download_resource(files_dir_path, img, url.strip(SLASH), SRC)

    for link in soup.find_all('link'):
        _download_resource(files_dir_path, link, url.strip(SLASH), HREF)

    for script in soup.find_all('script'):
        _download_resource(files_dir_path, script, url.strip(SLASH), SRC)
    return soup.prettify()


def download(url: str, output: str = 'current') -> str:
    """Do load web page and save to html file.

    Args:
        url (str): URL of requested web page.
        output (str): Path to directory to save.

    Returns:
        str: Path to saved file.
    """
    files_dir_path, output_html_path = make_paths(output, url.strip(SLASH))

    soup = make_soup(url)

    html_file = do_all_work(url, files_dir_path)

    write_to_file(output_html_path, html_file)
    return output_html_path
