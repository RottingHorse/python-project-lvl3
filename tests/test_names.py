import pytest
from page_loader.names import make_paths

FAKE_DIR_PATH = "/some_dir"
test_data = [
    (
        "https://ru.hexlet.io/courses",
        FAKE_DIR_PATH + "/ru-hexlet-io-courses.html",
        FAKE_DIR_PATH + "/ru-hexlet-io-courses_files",
    ),
    (
        "https://www.python.org",
        FAKE_DIR_PATH + "/www-python-org.html",
        FAKE_DIR_PATH + "/www-python-org_files",
    ),
    (
        "https://example.com",
        FAKE_DIR_PATH + "/example-com.html",
        FAKE_DIR_PATH + "/example-com_files",
    ),
]


@pytest.mark.parametrize(
    "url, html_file_name, files_dir_name",
    test_data,
)
def test_generated_html_name(url, html_file_name, files_dir_name) -> bool:
    assert files_dir_name, html_file_name == make_paths(FAKE_DIR_PATH, url)
