import pytest
from page_loader import url

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
    "address, html_file_name, files_dir_name",
    test_data,
)
def test_generated_html_name(address, html_file_name, files_dir_name):
    assert files_dir_name, html_file_name == url.to_paths(
        FAKE_DIR_PATH,
        address,
    )
