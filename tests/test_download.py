import os
import tempfile
import pyfakefs
import requests
import requests_mock
import filecmp
from page_loader.page_loader import create_file_path, create_dir, prepare_assets, create_resource_path, create_resource_url, save_resources


TEST_URL = 'https://ru.hexlet.io/courses'
TEST_IMG = 'https://ru.hexlet.io/assets/professions/nodejs.png'
TEST_HREF = 'https://ru.hexlet.io/assets/professions/nodejs'
TEST_HTML_NAME = 'ru-hexlet-io-courses.html'
IMG_DIR = 'ru-hexlet-io-courses_files'


def locate(file):
    return os.path.join('tests', 'fixtures', file)


def test_create_file_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        expected = os.path.join(tmpdir, 'ru-hexlet-io-courses.html')
        output = create_file_path(tmpdir, TEST_URL)
        assert output == expected


def test_create_dir(fs):
    assert IMG_DIR == create_dir(TEST_HTML_NAME)


def test_prepare_assets(fs):
    fs.add_real_directory(os.path.join('tests', 'fixtures'))
    fs.create_dir(IMG_DIR)
    with open(locate('test.html')) as f:
        input_html = f.read()
    assets, output_html = prepare_assets(input_html, TEST_URL, IMG_DIR)
    with open(locate('expected.html')) as f:
            expected = f.read()
    assert output_html == expected
    assert ('https://ru.hexlet.io/assets/application.css', 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css') in assets


def test_create_resource_path():
    expected_png = 'ru-hexlet-io-assets-professions-nodejs.png'
    expected_html = 'ru-hexlet-io-assets-professions-nodejs.html'
    output_img = create_resource_path(TEST_IMG)
    output_href = create_resource_path(TEST_HREF)
    assert expected_png == output_img
    assert expected_html == output_href


def test_create_resource_url():
    expected = 'https://ru.hexlet.io/assets/professions/nodejs.png'
    output = create_resource_url(TEST_URL, TEST_IMG)
    assert expected == output


def test_save_resources():
    assets = [('https://imgs.xkcd.com/comics/python.png', 'imgs-xkcd-com-comics-python.png')]
    with tempfile.TemporaryDirectory() as tmpdir:
        save_resources(tmpdir, assets)
        expected = locate('expected.bin')
        output = os.path.join(tmpdir, 'imgs-xkcd-com-comics-python.png')
        assert filecmp.cmp(expected, output)
        assert filecmp.cmp(expected, output, shallow=False)
