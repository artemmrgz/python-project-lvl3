import argparse
import os


def cli_parser():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('-o', '--output', type=str, default=os.getcwd(),
                        help=f'output dir (default: "{os.getcwd()}")')
    parser.add_argument('url', type=str, help='page url')
    return parser.parse_args()
