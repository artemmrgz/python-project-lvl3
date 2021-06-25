#!/usr/bin/env python3
from page_loader.page_loader import download
from page_loader.parser import cli_parser


def main():
    args = cli_parser()
    download(args.output, args.url)


if __name__ == '__main__':
    main()
