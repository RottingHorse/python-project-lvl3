"""File reader."""
from typing import Union


def get_content(path_to_file: str, flag: str) -> Union[str, bytes]:
    """Do read file.

    Args:
        path_to_file (str): Path to file
        flag (str): Mode flag, 'r' for text, 'rb' for bytes

    Returns:
        (str | bytes): File content
    """
    with open(path_to_file, flag) as file:
        return file.read()
