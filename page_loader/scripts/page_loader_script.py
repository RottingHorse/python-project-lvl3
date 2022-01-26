#!/usr/bin/env python
"""Page loader main script."""
import argparse
import logging
import sys

from page_loader import download
from page_loader.log import setup_log

UNIVERSAL_CODE = 42


def main():
    """Do run page loader."""
    setup_log()
    parser = argparse.ArgumentParser(description="Load web page")
    parser.add_argument(
        "-o",
        "--output",
        help="set output folder",
        default="current",
    )
    parser.add_argument("url")

    args = parser.parse_args()
    try:
        file_path = download(args.url, args.output)
    except Exception as err:
        logging.info(err)
        logging.error("Page was not downloaded!")
        sys.exit(UNIVERSAL_CODE)
    print(f"Page was successfully downloaded into '{file_path}'")


if __name__ == "__main__":
    main()
