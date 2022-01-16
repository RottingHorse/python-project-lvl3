import os
from urllib.parse import urlparse
from bs4.element import Tag


from page_loader.constants import DASH, DIR_SUFFIX, DOT, HTML_SUFFIX, SLASH


def make_name(url: str, end: str = '') -> str:
    """Do make filename or directory name from URL, depends on end.

    Args:
        url (str): URL to make name
        end (str): Last few characters of name. Defaults to ''.

    Returns:
        str: Name of file or directory
    """
    parsed_url = urlparse(url)

    return '{0}{1}{2}'.format(
        parsed_url.netloc.replace(DOT, DASH),
        parsed_url.path.replace(SLASH, DASH),
        end,
    )


def make_paths(output: str, url: str):
    """Do make paths for output HTML file and directory for files.

    Args:
        output (str): Base output directory
        url (str): Web page URL

    Returns:
        tuple(str): Directory path, HTML file path
    """
    if output == 'current':
        output_html_path = os.path.join(
            os.getcwd(),
            make_name(url, HTML_SUFFIX),
        )
        files_dir_path = os.path.join(os.getcwd(), make_name(url, DIR_SUFFIX))
    else:
        output_html_path = os.path.join(output, make_name(url, HTML_SUFFIX))
        files_dir_path = os.path.join(output, make_name(url, DIR_SUFFIX))
    return files_dir_path, output_html_path


def _is_same_domain(link_url: str, page_url: str) -> bool:
    parsed_link = urlparse(link_url)
    parsed_page = urlparse(page_url)
    return parsed_link.netloc == parsed_page.netloc


def generate_url(link: str, url: str) -> str:
    """Do generate url from 'src' or 'href' attribute

    Args:
        link (str): Link from attribute
        url (src): Web page index URL

    Returns:
        str: URL to download some resource
    """
    if 'jquery' in link:
        return None
    if not urlparse(link).scheme:
        return url + link
    if _is_same_domain(link, url):
        return link
    return None


def make_file_name(res_path: str, tag: Tag, base_url: str):
    """Do make file name for downloaded resource.

    Args:
        res_path (str): Source for file name
        tag (Tag): BeautifulSoup Tag
        base_url (str): Base URL for dir name

    Returns:
        str: Path to downloaded resource
    """
    if tag.name == 'script':
        tail = urlparse(res_path).path.replace(SLASH, DASH)
    else:
        tail = res_path.replace(SLASH, DASH)
    res_path = make_name(base_url) + tail
    if tag.name == 'link' and DOT not in res_path:
        res_path += HTML_SUFFIX
    return res_path
