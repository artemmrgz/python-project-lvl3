import os
import pytest
import requests
import requests_mock
import tempfile
from page_loader.page_loader import download, save_resources, PageLoadingError


BASE_URL = 'https://ru.hexlet.io/courses'


def test_except_download():
    with pytest.raises(FileNotFoundError):
        with tempfile.TemporaryDirectory() as tmpdir:
            with requests_mock.Mocker() as m:
                m.get(BASE_URL, text='data')
                download(os.path.join(tmpdir, 'abbglmg'), BASE_URL)



def test_except_save_resources():
    assets = [('https://imgs.xkcd.com/comics/python.png', 'imgs-xkcd-com-comics-python.png')]
    with pytest.raises(PageLoadingError):
        with tempfile.TemporaryDirectory() as tmpdir:
            with requests_mock.Mocker() as m:
                m.get('https://imgs.xkcd.com/comics/python.png', status_code=400)
                save_resources(BASE_URL, assets)


