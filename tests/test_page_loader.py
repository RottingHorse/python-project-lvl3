import os
import tempfile

import requests_mock

from page_loader.page_loader import download


def get_content(path_to_file):
    with open(path_to_file) as file:
        return file.read()


def test_page_loader():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as m:
            correct_data = get_content('tests/fixtures/correct_result.html')
            m.get('https://ru.hexlet.io/courses', text=correct_data)
            download('https://ru.hexlet.io/courses', tempdir)
            received_data = get_content(
                os.path.join(tempdir, 'ru-hexlet-io-courses.html'))
            assert received_data == correct_data
