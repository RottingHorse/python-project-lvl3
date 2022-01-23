"""Page loader main module."""
from page_loader.constants import SLASH
from page_loader.io import create_dir, write_to_file
from page_loader.log import logger
from page_loader.names import make_paths
from page_loader.web import get_from_url, prepare


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
            try:
                file_content = get_from_url(res_url)
            except Exception as err:
                logger.info(err)
                logger.warning(f"Can't download from {res_url}")
                continue
            if file_content:
                write_to_file(file_path, file_content)

    return output_html_path
