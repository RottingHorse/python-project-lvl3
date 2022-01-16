install:
	poetry install

uninstall:
	pip uninstall hexlet-code

page-loader:
	poetry run page-loader -h

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	rm -rf dist
	poetry build

.PHONY: install test lint selfcheck check build
