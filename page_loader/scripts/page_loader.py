#!/usr/bin/env python3
import sys
import logging
from page_loader.page_loader import download, PageLoadingError
from page_loader.parser import cli_parser


def main():
    args = cli_parser()
    try:
        result = download(args.url, args.output)
        print(f'Page was successfully downloaded into {result}')
    except PageLoadingError as err:
        logging.error(err)
        sys.exit(1)
    except FileExistsError:
        logging.error('Such file already exists')
        sys.exit(1)
    except FileNotFoundError:
        logging.error('No such file or directory')
    except PermissionError:
        logging.error('Lack of suitable permission to perform the action')
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
