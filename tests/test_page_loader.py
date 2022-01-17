import logging
import os
import tempfile
from http import HTTPStatus

import pytest
import requests
import requests_mock

from page_loader.page_loader import download

logger = logging.getLogger()

HTML_FILE = 'ru-hexlet-io-courses.html'
FILES_DIR = 'ru-hexlet-io-courses_files'
MAIN_URL = 'https://ru.hexlet.io'
PATH = '/courses'


def get_content(path_to_file, flag='r'):
    with open(path_to_file, flag) as file:
        return file.read()


def test_page_loader():
    with tempfile.TemporaryDirectory() as tempdir:
        correct_html = get_content('tests/fixtures/correct_result.html')
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL + PATH,
                     text=get_content('tests/fixtures/mock/HTML.html'))
            mock.get(
                MAIN_URL + '/assets/professions/nodejs.png',
                content=get_content('tests/fixtures/mock/nodejs.png', 'rb'))
            mock.get(MAIN_URL + '/assets/application.css',
                     text=get_content('tests/fixtures/mock/style.css'))
            mock.get(MAIN_URL + '/packs/js/runtime.js',
                     text=get_content('tests/fixtures/mock/script.js'))
            mock.get(MAIN_URL + '/no-resource.png',
                     status_code=HTTPStatus.NOT_FOUND)
            download(MAIN_URL + PATH, tempdir)
            received_html = get_content(
                os.path.join(tempdir, HTML_FILE))

            assert received_html == correct_html
            assert os.path.isfile(os.path.join(
                tempdir, FILES_DIR,
                'ru-hexlet-io-assets-professions-nodejs.png'))
            assert os.path.isfile(os.path.join(
                tempdir, FILES_DIR,
                'ru-hexlet-io-packs-js-runtime.js'))
            assert os.path.isfile(os.path.join(
                tempdir, FILES_DIR,
                'ru-hexlet-io-assets-application.css'))
            assert os.path.isfile(os.path.join(
                tempdir, FILES_DIR,
                'ru-hexlet-io-courses.html'))
            assert not os.path.isfile(os.path.join(
                tempdir, FILES_DIR, 'ru-hexlet-io-no-resource.png'))

            with pytest.raises(OSError):
                assert download(MAIN_URL + PATH, '/non_existing_dir')

            with pytest.raises(Exception):
                assert download(MAIN_URL + PATH, '/opt')


def test_page_loader_with_errors():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL + PATH, status_code=HTTPStatus.NOT_FOUND)
            assert not os.listdir(tempdir)
            with pytest.raises(requests.RequestException):
                download(MAIN_URL + PATH, tempdir)
            assert not os.listdir(tempdir)


def test_empty_page():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get('https://empty.com', text='<html></html>')
            download('https://empty.com', tempdir)
            assert os.path.isfile(os.path.join(tempdir, 'empty-com.html'))
            assert not os.path.isdir(os.path.join(tempdir, 'empty-com_files'))
