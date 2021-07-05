import os
import pytest
import tempfile
import pyfakefs
import requests
import requests_mock
import filecmp
from page_loader.page_loader import download, create_file_path, create_dir, prepare_assets, create_resource_path, create_resource_url, save_resources, PageLoadingError


BASE_URL = 'https://ru.hexlet.io/courses'
WITH_EXT = 'https://ru.hexlet.io/assets/professions/nodejs.png'
WITHOUT_EXT = 'https://ru.hexlet.io/assets/professions/nodejs'
FILE_NAME = 'ru-hexlet-io-courses.html'
DIR_NAME = 'ru-hexlet-io-courses_files'

LINKS = ['https://ru.hexlet.io/assets/application.css',
        'https://ru.hexlet.io/assets/professions/nodejs.png',
        'https://ru.hexlet.io/packs/js/runtime.js']
        


def locate(file):
    return os.path.join('tests', 'fixtures', file)


def test_download():
    with open(locate('test.html')) as f:
        data = f.read()
    with open(locate('expected.html')) as exp:
        expected = exp.read()
    with tempfile.TemporaryDirectory() as tmpdir:
        with requests_mock.Mocker() as m:
            m.get(BASE_URL, text=data)
            for link in LINKS:
                m.get(link, text='data')
            filepath = download(tmpdir, BASE_URL)
            file = os.path.join(tmpdir, FILE_NAME)
            with open(file) as fl:
                output = fl.read()
            assert filepath == file
            assert expected == output


def test_create_file_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        expected = os.path.join(tmpdir, 'ru-hexlet-io-courses.html')
        output = create_file_path(tmpdir, BASE_URL)
        assert output == expected


def test_create_dir(fs):
    assert DIR_NAME == create_dir(FILE_NAME)


def test_prepare_assets():
    with open(locate('test.html')) as f:
        input_html = f.read()
    with open(locate('expected.html')) as f:
            expected = f.read()

    assets, output_html = prepare_assets(input_html, BASE_URL, DIR_NAME)
    assert output_html == expected
    assert len(assets) == 4
    assert ('https://ru.hexlet.io/assets/application.css', 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css') in assets


def test_create_resource_path():
    expected_png = 'ru-hexlet-io-assets-professions-nodejs.png'
    expected_html = 'ru-hexlet-io-assets-professions-nodejs.html'
    output_img = create_resource_path(WITH_EXT)
    output_href = create_resource_path(WITHOUT_EXT)
    assert expected_png == output_img
    assert expected_html == output_href


def test_create_resource_url():
    expected = 'https://ru.hexlet.io/assets/professions/nodejs.png'
    output = create_resource_url(BASE_URL, WITH_EXT)
    assert expected == output


def test_save_resources():
    with open(locate('expected.bin'), 'rb') as f:
        content = f.read()
    assets = [('https://imgs.xkcd.com/comics/python.png', 'imgs-xkcd-com-comics-python.png')]
    with tempfile.TemporaryDirectory() as tmpdir:
        with requests_mock.Mocker() as m:
            m.get('https://imgs.xkcd.com/comics/python.png', content=content)
            save_resources(tmpdir, assets)
        output = os.path.join(tmpdir, 'imgs-xkcd-com-comics-python.png')
        with open(output, 'rb') as f:
            result = f.read()
    assert content == result
