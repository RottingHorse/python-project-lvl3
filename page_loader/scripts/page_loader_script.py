#!/usr/bin/env python
"""Page loader main script."""
import argparse

from page_loader import download


def main():
    """Do run page loader."""
    parser = argparse.ArgumentParser(description='Load web page')
    parser.add_argument('--output', help='set output folder', default='current')
    parser.add_argument('url')

    args = parser.parse_args()

    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
