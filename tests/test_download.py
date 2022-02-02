import os
from http import HTTPStatus
import tempfile

import pytest
import requests
import requests_mock
from page_loader.page_loader import download
from tests.reader import get_content

FILES_COUNT = 4
FILES_DIR = "ru-hexlet-io-courses_files"
HTML_FILE = "ru-hexlet-io-courses.html"
MAIN_URL = "https://ru.hexlet.io"
MOCK_DIR = "tests/fixtures/mock/"
PATH = "/courses"


main_html = get_content(os.path.join(MOCK_DIR, "HTML.html"), "r")
inner_html = get_content(os.path.join(MOCK_DIR, "inner.html"), "r")
png = get_content(os.path.join(MOCK_DIR, "nodejs.png"), "rb")
css = get_content(os.path.join(MOCK_DIR, "style.css"), "r")
js = get_content(os.path.join(MOCK_DIR, "script.js"), "r")

test_data = [
    (png, "ru-hexlet-io-assets-professions-nodejs.png", "rb"),
    (js, "ru-hexlet-io-packs-js-runtime.js", "r"),
    (css, "ru-hexlet-io-assets-application.css", "r"),
    (inner_html, "ru-hexlet-io-courses.html", "r"),
]


@pytest.mark.parametrize("file, file_name, flag", test_data)
def test_html_and_folder(file, file_name, flag):
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL + PATH, text=main_html)
            mock.get(
                MAIN_URL + "/assets/professions/nodejs.png",
                content=png,
            )
            mock.get(
                MAIN_URL + "/assets/application.css",
                text=css,
            )
            mock.get(
                MAIN_URL + "/packs/js/runtime.js",
                text=js,
            )
            mock.get(
                MAIN_URL + "/no-resource.png",
                status_code=HTTPStatus.NOT_FOUND,
            )
            download(MAIN_URL + PATH, tempdir)

            correct_html = get_content("tests/fixtures/correct_result.html", "r")
            received_html = get_content(os.path.join(tempdir, HTML_FILE), "r")

            assert received_html == correct_html

            files_count = len(os.listdir(os.path.join(tempdir, FILES_DIR)))
            assert files_count == FILES_COUNT

            file_path = os.path.join(tempdir, FILES_DIR, file_name)
            assert os.path.isfile(file_path)
            assert file == get_content(file_path, flag)


def test_non_existing_dir():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL, text="<html></html>")
            with pytest.raises(Exception):
                download(MAIN_URL, tempdir + "/non_existing_dir")


def test_download_with_errors():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL, status_code=HTTPStatus.NOT_FOUND)
            assert not os.listdir(tempdir)
            with pytest.raises(requests.RequestException):
                download(MAIN_URL, tempdir)
            assert not os.listdir(tempdir)


def test_empty_page():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL, text="<html></html>")

            download(MAIN_URL, tempdir)

            assert os.path.isfile(os.path.join(tempdir, "ru-hexlet-io.html"))
            assert not os.path.isdir(os.path.join(tempdir, "ru-hexlet-io_files"))
