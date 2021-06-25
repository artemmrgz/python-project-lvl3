import os
import tempfile
import requests
import requests_mock
from page_loader.page_loader import download, create_path


TEST_URL = 'https://ru.hexlet.io/courses'
TEST_DATA = 'Some data'


def test_download():
    with tempfile.TemporaryDirectory() as tmpdir:
        with requests_mock.Mocker() as m:
            m.get(TEST_URL, text=TEST_DATA)
            download(tmpdir, TEST_URL)
        with open(create_path(tmpdir, TEST_URL), 'r') as f:
            output = f.read()
    assert output == TEST_DATA
