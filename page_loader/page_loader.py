"""Page loader main module."""
import logging
from typing import Union

import requests
from page_loader import url
from page_loader.constants import SLASH
from page_loader.html import prepare
from page_loader.io import create_dir, write_to_file
from progress.bar import ChargingBar


def _get(address: str) -> Union[str, bytes]:
    response = requests.get(address)
    response.raise_for_status()
    logging.info(f"Resource from {address} was downloaded")
    return response.content


def download(address: str, output: str = "current") -> str:
    """Do load web page and save to html file.

    Args:
        address (str): URL of requested web page.
        output (str): Path to directory to save.

    Returns:
        str: Path to saved file.
    """
    files_dir_path, output_html_path = url.to_paths(
        output,
        address.strip(SLASH),
    )
    raw_html = _get(address.strip(SLASH))
    html_file, resources = prepare(
        raw_html,
        files_dir_path,
        address.strip(SLASH),
    )
    write_to_file(output_html_path, html_file)

    if resources:
        create_dir(files_dir_path)
        progress_bar = ChargingBar(max=len(resources))
        for res_url, file_path in resources:
            progress_bar.message = f"{res_url}\n"
            progress_bar.next()
            try:
                file_content = _get(res_url)
            except Exception as err:
                logging.info(err)
                logging.warning(f"Can't download from {res_url}")
                continue
            if file_content:
                write_to_file(file_path, file_content)
        progress_bar.finish()

    return output_html_path
