"""Page loader."""
import os

import requests


def _make_file_name(url: str) -> str:
    filename = url.replace('https://', '')
    filename = filename.replace('/', '-')
    filename = filename.replace('.', '-')
    return '{0}{1}'.format(filename, '.html')


def download(url: str, output='current') -> str:
    """Do load web page and save to html file.

    Args:
        url (str): URL of requested web page.
        output (srt): Path to directory to save.

    Returns:
        str: Path to saved file.
    """
    if output == 'current':
        output_path = os.path.join(os.getcwd(), _make_file_name(url))
    else:
        output_path = os.path.join(output, _make_file_name(url))
    response = requests.get(url)
    response.raise_for_status()
    html_data = response.text
    with open(output_path, 'w') as out_file:
        out_file.write(html_data)

    return output_path
