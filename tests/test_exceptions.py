import os
import pytest
import requests_mock
import tempfile
from page_loader.page_loader import download, save_resources, PageLoadingError


BASE_URL = 'https://ru.hexlet.io/courses'
ASSETS = [('https://imgs.xkcd.com/comics/python.png',
           'imgs-xkcd-com-comics-python.png')]


def test_except_download():
    with pytest.raises(FileNotFoundError):
        with tempfile.TemporaryDirectory() as tmpdir:
            with requests_mock.Mocker() as m:
                m.get(BASE_URL, text='data')
                download(BASE_URL, os.path.join(tmpdir, 'abbglmg'))


def test_except_save_resources():
    with pytest.raises(PageLoadingError):
        with requests_mock.Mocker() as m:
            m.get('https://imgs.xkcd.com/comics/python.png', status_code=400)
            save_resources(BASE_URL, ASSETS)
