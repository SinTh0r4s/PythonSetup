import os.path
import subprocess
import sys
from argparse import ArgumentParser, BooleanOptionalAction

import pytest
from _pytest.config import ExitCode
from coverage import Coverage

_project_name = "MyProject"
_project_directory = "myproject"


def format_and_sort() -> None:
    parser = ArgumentParser()
    parser.add_argument("-dry", action=BooleanOptionalAction, help="Does not change the code base")
    args = parser.parse_args()
    flags = [] if args.dry is None else ["--check"]

    print("Starting black...")  # noqa: T201
    black_result = subprocess.run(["poetry", "run", "black", "."] + flags)

    print("Starting isort...")  # noqa: T201
    isort_result = subprocess.run(["poetry", "run", "isort", "."] + flags)

    exit(black_result.returncode or isort_result.returncode)


def check() -> None:
    print("Starting flake8...")  # noqa: T201
    flake8_result = subprocess.run(["poetry", "run", "flake8", "."])

    print("Starting mypy...")  # noqa: T201
    mypy_result = subprocess.run(["poetry", "run", "mypy", "."])

    exit(flake8_result.returncode or mypy_result.returncode)


def _run_tests(directory: str) -> int | ExitCode:
    return pytest.main([os.path.join(os.path.dirname(__file__), directory)])


def test() -> None:
    print("Starting unit tests...")  # noqa: T201
    if not _run_tests(_project_directory) == ExitCode.OK:
        exit(1)


def integration_test() -> None:
    print("Starting integration tests...")  # noqa: T201
    if not _run_tests("integration_tests") == ExitCode.OK:
        exit(1)


def _run_coverage() -> Coverage:
    coverage = Coverage(source=[_project_directory], branch=True, omit=["**/test_*.py"])
    coverage.start()
    _run_tests(_project_directory)
    coverage.stop()
    return coverage


def coverage() -> None:
    result = _run_coverage()
    print("Reporting coverage...")  # noqa: T201
    total_coverage_percent = result.report(skip_covered=True, skip_empty=True)
    if total_coverage_percent < 100:
        print(  # noqa: T201
            f"Coverage not sufficient! Only {total_coverage_percent:.2f}%, but full coverage required!",
            file=sys.stderr,
        )
        exit(1)


def coverage_html() -> None:
    result = _run_coverage()
    print("Rendering HTML coverage report...")  # noqa: T201
    result.html_report(skip_covered=True, skip_empty=True, title=f"Coverage Report - {_project_name}")
