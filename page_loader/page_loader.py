import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')


tags = {'img': 'src', 'link': 'href', 'script': 'src'}
MAX_FILENAME_LENGTH = 25
MAX_RESOURCE_NAME_LENGTH = 50


def download(path_to_dir, base_url):
    file_path = create_file_path(path_to_dir, base_url)
    logging.debug(f'File path - {file_path}')
    files_dir = create_dir(file_path)
    html_file = requests.get(base_url).text
    logging.debug(f'Get request to {base_url}')
    assets, changed_file = prepare_assets(html_file, base_url, files_dir)
    save_file(file_path, changed_file)
    save_resources(files_dir, assets)


def create_file_path(path_to_dir, base_url):
    url_parts = re.split('[^0-9a-zA-z]+', base_url)
    url_parts.pop(0)
    filename = '-'.join(url_parts)[:MAX_FILENAME_LENGTH] + '.html'
    return os.path.join(path_to_dir, filename)


def create_dir(path_to_file):
    path_parts = os.path.splitext(path_to_file)
    dir_ = path_parts[0] + '_files'
    logging.warning(f'dir {dir_} is about to be created,\
                    dir with such name shouldn\'t exist')
    os.mkdir(dir_)
    return dir_


def prepare_assets(html, base_url, files_dir):
    soup = BeautifulSoup(html, 'html.parser')
    assets = []
    resources = filter(lambda x: is_local(base_url, x), soup.find_all(tags))
    for resource in resources:
        tag = tags[resource.name]
        resource_url = create_resource_url(base_url, resource.get(tag))
        logging.debug(f'Resource url - {resource_url}')
        resource_path = os.path.join(files_dir,
                                     create_resource_path(resource_url))
        logging.debug(f'Resource path - {resource_path}')
        assets.append((resource_url, resource_path))
        resource[tag] = resource_path
    return assets, soup.prettify(formatter="html5")


def is_local(base_url, tag):
    url_ = tag.get(tags[tag.name])
    if url_:
        netloc = urlparse(base_url).netloc
        return (url_[0] == '/' and url_[1] != '/') or netloc in url_


def create_resource_path(resource_url):
    path, extension = os.path.splitext(resource_url)
    if not extension:
        extension = '.html'
    url_parts = re.split('[^0-9a-zA-Z]+', path)
    url_parts.pop(0)
    return '-'.join(url_parts)[:MAX_RESOURCE_NAME_LENGTH] + extension


def create_resource_url(base_url, resource_url):
    parsed_url = urlparse(base_url)
    parsed_resource = urlparse(resource_url)
    new_url = parsed_resource._replace(scheme=parsed_url[0],
                                       netloc=parsed_url[1])
    return new_url.geturl()


def save_resources(files_dir, assets):
    for url, path in assets:
        path_to_file = os.path.join(files_dir, path)
        with open(path_to_file, 'wb') as f:
            f.write(requests.get(url).content)


def save_file(save_to, page):
    with open(save_to, 'w') as f:
        f.write(page)
