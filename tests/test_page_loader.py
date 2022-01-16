import logging
import os
import tempfile
from http import HTTPStatus

import pytest
import requests_mock

from page_loader.page_loader import download

logger = logging.getLogger()


def get_content(path_to_file, flag='r'):
    with open(path_to_file, flag) as file:
        return file.read()


def test_page_loader():
    with tempfile.TemporaryDirectory() as tempdir:
        correct_html = get_content('tests/fixtures/correct_result.html')
        with requests_mock.Mocker() as mock:
            mock.get('https://ru.hexlet.io',
                     text=get_content('tests/fixtures/mock/HTML.html'))
            mock.get(
                'https://ru.hexlet.io/assets/professions/nodejs.png',
                content=get_content('tests/fixtures/mock/nodejs.png', 'rb'))
            mock.get('https://ru.hexlet.io/courses',
                     text=get_content('tests/fixtures/mock/inner.html'))
            mock.get('https://ru.hexlet.io/assets/application.css',
                     text=get_content('tests/fixtures/mock/style.css'))
            mock.get('https://ru.hexlet.io/packs/js/runtime.js',
                     text=get_content('tests/fixtures/mock/script.js'))
            download('https://ru.hexlet.io/', tempdir)
            received_html = get_content(
                os.path.join(tempdir, 'ru-hexlet-io.html'))

            assert received_html == correct_html
            assert os.path.isfile(os.path.join(
                tempdir, 'ru-hexlet-io_files',
                'ru-hexlet-io-assets-professions-nodejs.png'))
            assert os.path.isfile(os.path.join(
                tempdir, 'ru-hexlet-io_files',
                'ru-hexlet-io-packs-js-runtime.js'))
            assert os.path.isfile(os.path.join(
                tempdir, 'ru-hexlet-io_files',
                'ru-hexlet-io-assets-application.css'))
            assert os.path.isfile(os.path.join(
                tempdir, 'ru-hexlet-io_files',
                'ru-hexlet-io-courses.html'))

            with pytest.raises(SystemExit) as err:
                download('https://ru.hexlet.io/', '/non_existing_dir')
                assert err.value.code == 42
            with pytest.raises(SystemExit) as err:
                download('https://ru.hexlet.io/', '/opt')
                assert err.value.code == 42


def test_page_loader_with_errors(caplog):

    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get('https://ru.hexlet.io', status_code=HTTPStatus.NOT_FOUND)
            with caplog.at_level(logging.ERROR):
                download('https://ru.hexlet.io', tempdir)
            assert 'None for url' in caplog.text
