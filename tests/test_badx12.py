#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `badx12` package."""

import collections
import shutil

import pytest
from click.testing import CliRunner

from badx12 import Parser
from badx12 import cli
from badx12.common.click import add_commands
from badx12.utils import errors as err
from tests.utils import TEST_FILE_DIR, TEST_TEMP_FILE_DIR


@pytest.fixture
def test_files():
    return {
        "edi": list((TEST_FILE_DIR / "edi").glob("*.edi")),
        "errors": TEST_FILE_DIR / "errors",
    }


@pytest.fixture()
def cli_runner():
    return CliRunner()


def test_cli(test_files, cli_runner):
    good_files = test_files["edi"]
    bad_files = test_files["errors"].glob("*.edi")

    for ext in ["json", "xml"]:
        for f in good_files:
            TEST_TEMP_FILE_DIR.mkdir()
            result = cli_runner.invoke(
                cli,
                [
                    "parse",
                    f"{f}",
                    f"--output_dir={TEST_TEMP_FILE_DIR}",
                    f"--export_type={ext.upper()}",
                ],
            )
            file_count = collections.Counter(
                p.suffix for p in TEST_TEMP_FILE_DIR.iterdir()
            )

            assert result.exit_code == 0
            assert result.output == ""
            assert file_count[f".{ext}"] == 1

            shutil.rmtree(TEST_TEMP_FILE_DIR)

        for f in bad_files:
            TEST_TEMP_FILE_DIR.mkdir()
            result = cli_runner.invoke(
                cli,
                [
                    "parse",
                    f"{f}",
                    f"--output_dir={TEST_TEMP_FILE_DIR}",
                    f"--export_type={ext.upper()}",
                ],
            )

            assert result.exit_code == 0

            shutil.rmtree(TEST_TEMP_FILE_DIR)


def test_click_common():
    with pytest.raises(TypeError, message="Expected TypeError"):
        add_commands("cli", "commands")

    with pytest.raises(TypeError, message="Expected TypeError"):
        add_commands(cli, None)

    with pytest.raises(TypeError, message="Expected TypeError"):
        add_commands(cli, ("command", "command"))


def test_edi(test_files):
    files = test_files["edi"]
    assert len(files) > 0

    for file in files:
        parser = Parser(file)

        assert parser.document.text != ""
        assert parser.document.interchange is not None

        report = parser.document.validate()
        assert report.is_document_valid() is True
        assert len(report.error_list) == 0
        assert parser.document.format_as_edi() != ""


def test_bad_file(test_files):
    with pytest.raises(
        err.InvalidFileTypeError, message="Expecting InvalidFileTypeError"
    ):
        Parser((test_files["errors"] / "bad_file.edi"))


def test_segment_terminator(test_files):
    with pytest.raises(
        err.SegmentTerminatorNotFoundError,
        message="Expected SegmentTerminatorNotFoundError",
    ):
        Parser((test_files["errors"] / "segment_terminator.edi"))


def test_error_validation(test_files):
    parser = Parser((test_files["errors"] / "error_validation.edi"))
    report = parser.document.validate()

    assert len(report.error_list) > 0
    assert report.is_document_valid() is False


def test_bad_file_input():
    with pytest.raises(TypeError, message="Expected TypeError"):
        Parser(TEST_FILE_DIR)


def test_coverage(test_files):
    parser = Parser((test_files["errors"] / "unknown_segment_error.edi"))
    repr(parser.document)
    str(parser.document.interchange.header)
