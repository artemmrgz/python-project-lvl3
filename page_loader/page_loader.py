import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def download(path_to_dir, page_url):
    file_path = create_path(path_to_dir, page_url)
    img_dir = create_img_dir(file_path)
    html_file = requests.get(page_url).text
    changed_file = change_links_and_save_imgs(html_file, page_url, img_dir)
    save_file(file_path, changed_file)


def create_path(path_to_dir, url):
    url_parts = re.split('[^0-9a-zA-Z]+', url)
    url_parts.pop(0)
    filename = '-'.join(url_parts)[:25] + '.html'
    return os.path.join(path_to_dir, filename)


def create_img_dir(path_to_file):
    path_parts = os.path.splitext(path_to_file)
    dir_ = path_parts[0] + '_files'
    os.mkdir(dir_)
    return dir_


def change_links_and_save_imgs(html, page_url, img_dir):
    soup = BeautifulSoup(html, 'html.parser')

    for img in soup.find_all('img'):
        img_url = create_img_url(page_url, img['src'])
        img_path = create_img_path(img_dir, img_url)
        save_img(img_path, img_url)
        img['src'] = img_path
    print(soup.prettify(formatter="html5"))
    return soup.prettify(formatter="html5")


def create_img_path(img_dir, img_url):
    without_extension = os.path.splitext(img_url)[0]
    url_parts = re.split('[^0-9a-zA-Z]+', without_extension)
    url_parts.pop(0)
    img_name = '-'.join(url_parts)[:50] + '.png'
    return os.path.join(img_dir, img_name)


def create_img_url(page_url, img_url):
    parsed_url = urlparse(page_url)
    parsed_img_url = urlparse(img_url)
    starting_from_path = parsed_img_url._replace(scheme='', netloc='')
    img_url = starting_from_path.geturl()
    return f'{parsed_url[0]}://{parsed_url[1]}{img_url}'


def save_img(save_to, img_url):
    with open(save_to, 'wb') as f:
        f.write(requests.get(img_url).content)


def save_file(save_to, page):
    with open(save_to, 'w') as f:
        f.write(page)
