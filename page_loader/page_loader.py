"""Page loader main module."""
import os

from page_loader.constants import ATTRIBUTES, DIR_SUFFIX, SLASH
from page_loader.io import create_dir, write_to_file
from page_loader.log import logger
from page_loader.names import (
    generate_url,
    make_file_name,
    make_name,
    make_paths,
)
from page_loader.web import get_from_url, prepare
from progress.bar import ChargingBar


# def _get_resource(file_path: str, tag: Tag, base_url, attr):
#     try:
#         res_path = tag[attr]
#     except KeyError:
#         return None
#     res_url = generate_url(res_path, base_url)
#     if res_url is None:
#         return None
#     try:
#         res_content = get_from_url(res_url)
#     except requests.RequestException as err:
#         logger.info(err)
#         logger.warning(f"Can't download from {res_url}")
#         return None
#     res_path = make_file_name(res_path, tag, base_url)
#     full_path = os.path.join(res_path, file_path, res_path)
#     new_src = os.path.join(make_name(base_url, DIR_SUFFIX), res_path)
#     tag[attr] = new_src
#     return res_content, full_path


# def _get_tags(tags, files_dir_path: str, url: str):
#     progress_bar = ChargingBar(message=f"Loading {url}", max=len(tags))
#     tags_content = []
#     for tag in tags:
#         attr_name = ATTRIBUTES[tag.name]
#         payload = _get_resource(files_dir_path, tag, url, attr_name)
#         if payload is not None:
#             tags_content.append(payload)
#         progress_bar.next()
#     progress_bar.finish()
#     return tags_content


def download(url: str, output: str = "current") -> str:
    """Do load web page and save to html file.

    Args:
        url (str): URL of requested web page.
        output (str): Path to directory to save.

    Returns:
        str: Path to saved file.
    """
    files_dir_path, output_html_path = make_paths(output, url.strip(SLASH))
    html_file, resources = prepare(url.strip(SLASH), files_dir_path)
    write_to_file(output_html_path, html_file)

    if resources:
        create_dir(files_dir_path)

        for res_url, file_path in resources:
            file_content = get_from_url(res_url)
            write_to_file(file_path, file_content)

    return output_html_path
