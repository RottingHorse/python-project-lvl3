"""Page loader main module."""
from page_loader.constants import SLASH
from page_loader.io import create_dir, make_paths, write_to_file
from page_loader.web import do_all_work


def download(url: str, output: str = 'current') -> str:
    """Do load web page and save to html file.

    Args:
        url (str): URL of requested web page.
        output (str): Path to directory to save.

    Returns:
        str: Path to saved file.
    """
    files_dir_path, output_html_path = make_paths(output, url.strip(SLASH))

    create_dir(files_dir_path)

    html_file = do_all_work(url, files_dir_path)

    write_to_file(output_html_path, html_file)
    return output_html_path
