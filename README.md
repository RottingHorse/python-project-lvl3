### Hexlet tests and linter status:

[![Actions Status](https://github.com/EvilMadSquirrel/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/EvilMadSquirrel/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/b0b4eefb1ef06b91d4e3/maintainability)](https://codeclimate.com/github/EvilMadSquirrel/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b0b4eefb1ef06b91d4e3/test_coverage)](https://codeclimate.com/github/EvilMadSquirrel/python-project-lvl3/test_coverage)
[![Python CI](https://github.com/EvilMadSquirrel/python-project-lvl3/actions/workflows/pyci.yml/badge.svg)](https://github.com/EvilMadSquirrel/python-project-lvl3/actions/workflows/pyci.yml)


# Page loader
### Console utility for downloading web pages
---
## Installation:

```bash
pip install --user git+https://github.com/EvilMadSquirrel/python-project-lvl3
```

## Usage

### As a library:

```python
from page_loader import download

file_path = download('https://example.com', '/var/tmp')
print(file_path)  # => '/var/tmp/example-com.html'
```

### As a console utility

```bash
$ page-loader -h
usage: page-loader [-h] [--output OUTPUT] url

Load web page

positional arguments:
  url

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  set output folder


$ page-loader --output /var/tmp https://ru.hexlet.io/courses
/var/tmp/ru-hexlet-io-courses.html
```

## Example:

[![asciicast](https://asciinema.org/a/462073.svg)](https://asciinema.org/a/462073)
