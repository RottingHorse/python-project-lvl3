import os
import tempfile

from page_loader.page_loader import download


def get_content(path_to_file):
    with open(path_to_file) as file:
        return file.read()


def test_page_loader():
    with tempfile.TemporaryDirectory() as tempdir:
        correct_html = get_content('tests/fixtures/correct_result.html')
        download('https://page-loader.hexlet.repl.co', tempdir)
        received_html = get_content(
            os.path.join(tempdir, 'page-loader-hexlet-repl-co.html'))

        assert received_html == correct_html
        assert os.path.isfile(os.path.join(
            tempdir, 'page-loader-hexlet-repl-co_files',
            'page-loader-hexlet-repl-co-assets-professions-nodejs.png'))
