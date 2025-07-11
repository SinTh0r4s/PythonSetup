# MyProject

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![pr-checks](https://github.com/SinTh0r4s/PythonSetup/workflows/pr-checks/badge.svg)](https://github.com/SinTh0r4s/PythonSetup/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-green)](https://github.com/cariad-t2/TraceK.PY-SDK/actions/workflows/pr-check.yml)
[![mypy badge](https://www.mypy-lang.org/static/mypy_badge.svg)](https://github.com/python/mypy)
[![Linting: flake8](https://img.shields.io/badge/linting-flake8-ffffff.svg)](https://github.com/PyCQA/flake8)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


### Setup

- Supported IDEs: ![PyCharm](https://img.shields.io/badge/PyCharm-000?logo=pycharm&logoColor=fff) ![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/Visual%20Studio%20Code-0078d7.svg?logo=vsc&logoColor=white)
- You need at least Python `3.12`. This project was developed on that version, although newer versions *should* work as well. Verify your version with `python --version`.
- Install `poetry`. It is a package manager and used by TraceK.PY and should be installed globally: `pip install poetry`. It will now be available in your terminal as `poetry`
- Clone this repository and open the root directory in a terminal. Then run `poetry install` on any command line.
- If you run VS Code: install the recommended extensions for formatting and linting.
- That's already it!


**Known issues:**

- `poetry install` might not find your python 3.12+ installation. In that case you need to [explicitly link it](https://python-poetry.org/docs/managing-environments/#switching-between-environments) before executing `poetry install` again.


### Custom dev commands

- `poetry run format` invokes black and isort to format the code base.
- `poetry run check` invokes flake8 for linting and mypy for static type checking.
- `poetry run test` invokes pytest to run all the unit-tests. A unit test filename must satisfy the prefix `test_*.py` and every test function must equally satisfy the prefix `def test_*()`. This is the industry-wide default behaviour.
- `poetry run integration-test` invokes pytest to run all integration-tests.
- `poetry run coverage` invokes coverage and reports all non-covered files of the framework.
- `poetry run coverage-html` like `coverage`, but creates a HTML report with more details.
