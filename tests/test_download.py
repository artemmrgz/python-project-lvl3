import os
import tempfile
import pyfakefs
import requests
import requests_mock
import filecmp
from page_loader.page_loader import create_path, create_img_dir, change_links_and_save_imgs, create_img_path, create_img_url


TEST_URL = 'https://ru.hexlet.io/courses'
TEST_IMG_NAME = '/assets/professions/nodejs.png'
FULL_IMG_URL = 'https://ru.hexlet.io//assets/professions/nodejs.png'
TEST_HTML_NAME = 'ru-hexlet-io-courses.html'
IMG_DIR = 'ru-hexlet-io-courses_files'
TEST_IMG_URL = '/derivations/image/fill_webp/540/320/eyJpZCI6Ijk4YjY4ODdjMjVlOTI1OWVjOWQ0MDFkNzc3O' \
               'TEwNWM4LnBuZyIsInN0b3JhZ2UiOiJzdG9yZSJ9?signature=8b9d21429f1b423628e7a9c4521839809652b4a7f05db0bc83d4' \
               '5b6bf2658d14'


def locate(file):
    return os.path.join('tests', 'fixtures', file)


def test_create_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        expected = os.path.join(tmpdir, 'ru-hexlet-io-courses.html')
        output = create_path(tmpdir, TEST_URL)
        assert output == expected


def test_create_img_dir(fs):
    assert IMG_DIR == create_img_dir(TEST_HTML_NAME)


def test_change_links_and_save_imgs(fs):
    fs.create_dir(IMG_DIR)
    fs.add_real_directory(os.path.join('tests', 'fixtures'))
    with open(locate('test.html')) as f:
        input_html = f.read()
    with open(locate('expected.bin'), 'rb') as file:
        expected_img = file.read()
    with requests_mock.Mocker() as m:
        m.get(TEST_IMG_URL, content=expected_img)
        output_html = change_links_and_save_imgs(input_html, TEST_URL, IMG_DIR)
    img_file = os.path.join(IMG_DIR, 'ru-hexlet-io-derivations-image-fill-webp-540-320-e.png')
    with open(locate('expected.html')) as f:
            expected = f.read()
    assert os.path.exists(img_file)
    assert output_html == expected
    assert filecmp.cmp(locate('expected.bin'), img_file)
    assert filecmp.cmp(locate('expected.bin'), img_file, shallow=False)


def test_create_img_path():
    expected = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
    output = create_img_path(IMG_DIR, FULL_IMG_URL)
    assert expected == output


def test_create_img_url():
    expected = 'https://ru.hexlet.io/assets/professions/nodejs.png'
    output = create_img_url(TEST_URL, TEST_IMG_NAME)
    assert expected == output
