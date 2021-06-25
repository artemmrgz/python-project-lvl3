import os
import re
import requests


def download(path_to_dir, url):
    file_path = create_path(path_to_dir, url)
    text = get_page_data(url)
    save_data(file_path, text)


def create_path(path_to_dir, url):
    url_parts = re.split('[^0-9a-zA-z]+', url)
    url_parts.pop(0)
    filename = '-'.join(url_parts) + '.html'
    return os.path.join(path_to_dir, filename)


def get_page_data(url):
    page = requests.get(url)
    return page.text


def save_data(location, page):
    with open(location, 'w') as f:
        f.write(page)
