import requests_mock

from tests.reader import get_content
from page_loader.web import prepare


FAKE_DIR_PATH = "/some_dir"


def test_processed_html():
    correct_html = get_content("tests/fixtures/correct_result.html", "r")
    raw_html = get_content("tests/fixtures/mock/HTML.html", "r")

    with requests_mock.Mocker() as mock:
        mock.get("https://ru.hexlet.io/courses", text=raw_html)
        processed_html, _ = prepare("https://ru.hexlet.io/courses", FAKE_DIR_PATH)

    assert processed_html == correct_html
