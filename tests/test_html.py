from tests.reader import get_content
from page_loader.html import prepare


FAKE_DIR_PATH = "/some_dir"
FAKE_URL = "https://ru.hexlet.io/courses"


def test_processed_html():
    correct_html = get_content("tests/fixtures/correct_result.html", "r")
    raw_html = get_content("tests/fixtures/mock/HTML.html", "r")

    processed_html, _ = prepare(raw_html, FAKE_DIR_PATH, FAKE_URL)

    assert processed_html == correct_html
