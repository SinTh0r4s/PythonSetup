# TraceK.PY

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![pr-checks](https://github.com/cariad-t2/TraceK.PY/workflows/pr-checks/badge.svg)](https://github.com/cariad-t2/TraceK.PY/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-green)](https://github.com/cariad-t2/TraceK.PY-SDK/actions/workflows/pr-check.yml)
[![mypy badge](https://www.mypy-lang.org/static/mypy_badge.svg)](https://github.com/python/mypy)
[![Linting: flake8](https://img.shields.io/badge/linting-flake8-ffffff.svg)](https://github.com/PyCQA/flake8)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License: CARIAD](https://img.shields.io/badge/license-CARIAD-442EE0.svg)](LICENSE)


![TraceK.PY - Overview](./docs/tracek.py-overview.png)

TraceK.PY introduces two abstract layers on top of the existing car logs: [Live data](./docs/live_data_format.md) and [post-drive data](./docs/post-drive_format.md). Live data is what common monitoring systems provide. Since all our analytics are done after the drive, it introduces the post-drive layer to reduce the data footprint and make the data more efficient and easier to use. The aggregation from live data to post-drive data is fully automatic. 

>The usability of monitoring data limits the scope of feasible implementations for analytics. Ease of use is the key enable to create advance insights into our product development!

### Using TraceK.PY results

Take a look at an overview of the [post-drive data format](./docs/post-drive_format.md). You may use a result provided to you or run the framework yourself. (See [setup](#setup) and [analyzing a log](#analyzing-a-log))


### Setup

- Supported IDEs: ![PyCharm](https://img.shields.io/badge/PyCharm-000?logo=pycharm&logoColor=fff) ![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/Visual%20Studio%20Code-0078d7.svg?logo=vsc&logoColor=white)
- You need at least Python `3.12`. It was developed on that version, although newer versions *should* work as well. Verify your version with `python --version`. If necessary, Python 3.12 can be installed via Baramundi.
- Install `poetry`. It is a package manager and used by TraceK.PY and should be installed globally: `pip install poetry`. It will now be available in your terminal as `poetry`
- Clone this repository and open the root directory in a terminal. Then run `poetry install` on any command line.
- If you run VS Code: install the recommended extensions for formatting and linting.
- That's already it!


**Known issues:**

- You might not get any dependencies installed. You need to set up your local Python installation to work in the VW IT system.
- `poetry install` might not find your python 3.12+ installation. In that case you need to [explicitly link it](https://python-poetry.org/docs/managing-environments/#switching-between-environments) before executing `poetry install` again.


### Analyzing a log

 You can invoke a CLI via `poetry run python cli.py <arguments>`. Just run it without arguments to get help printed


### Custom dev commands

- `poetry run format` invokes black and isort to format the code base.
- `poetry run check` invokes flake8 for linting and mypy for static type checking.
- `poetry run test` invokes py-test to run all the unit-tests. A unit test filename must satisfy the prefix `test_*.py` and every test function must equally satisfy the prefix `def test_*()`. This is the industry-wide default behaviour.
- `poetry run integration-test` invokes py-test to run all the integration-tests. These tests will not fail based on code from namespaces and are solely intended for the framework development.
- `poetry run coverage` invokes coverage and reports all non-covered files of the framework. *All namespaces are ignored! (only coverage; unit-tests are executed anyway)*.
- `poetry run coverage-html` like `coverage`, but creates a HTML report with more details.


## Working with TraceK.PY
### Upcycling

![TraceK.PY - Upcycling](./docs/tracek.py-upcycling.png)
TraceK.PY provides you with two options. You may take the log as is and implement parser(s) and transformer(s) to upcycle the log. This option allows you to get results quickly as no components on the car must be touched. The price you pay for this flexibility is inevitable maintenance whenever the log changes as the parser and transformer must be adjusted to continue to work.

How to implement [parsers](./docs/parsers_and_transformers#parsers) and [transformers](./docs/parsers_and_transformers#transformers).

### Structured Logging

![TraceK.PY - Structured Logging](./docs/tracek.py-structured-logging.png)
You may adapt the software on the car to use the [structured logging format](./docs/structured_logging_format_v1.md) to create monitoring data directly. This will be more elaborate to set up as you will need to synchronize with application development, but it will reward you with a maintenance free and reliable solution.


>### Best Practice
>
>Use structured logging wherever you know that data is used moderately frequently. You may implement upcycling to have data available immediately for use in analytics and then replace the upcycling with structured logging as soon as it is implemented in the car software. TraceK.PY will discard upcycling results if structured logging produces data with identical labels. This will provide a seemless transition between upcycling and structured logging and any analytics will continue to work without changes.


## Architecture Overview

TraceK.PY is a pipeline to process a stream of log items. This enables TraceK.PY to handle enormously large log files of 40GB as well as a livestream from the car (to be implemented as data source). The following diagram depicts the components of TraceK.PY with matching labels to the code such that a search will immediately find the correlating code. Green coloring shows the execution location of namespace upcycling.

![Architecture Overview](./docs/architecture_overview.png)

**Why are messages converted to UTC during `aggregate` and not earlier?** The System is quite often at the wrong time during development and must correct itself with received times. This may take some time and would block TraceK.PY to produce any `Live Data` until that happens (or the current time is confirmed as correct UTC). It is much simpler to take the last reported UTC time before the log ends as reference. This timestamp will be valid UTC if there was any correction.
