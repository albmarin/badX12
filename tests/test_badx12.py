#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `badx12` package."""

import pytest

from badx12 import Parser
from badx12.utils import errors as err
from tests.utils import X12_DIR


@pytest.fixture
def x12_files():
    return {"edi": list((X12_DIR / "edi").glob("*.edi")), "errors": X12_DIR / "errors"}


def test_edi(x12_files):
    files = x12_files["edi"]
    assert len(files) > 0

    for file in files:
        parser = Parser(file)

        assert parser.document.text != ""
        assert parser.document.interchange is not None

        report = parser.document.validate()
        assert report.is_document_valid() is True
        assert len(report.error_list) == 0
        assert parser.document.format_as_edi() != ""


def test_bad_file(x12_files):
    with pytest.raises(
        err.InvalidFileTypeError, message="Expecting InvalidFileTypeError"
    ):
        Parser((x12_files["errors"] / "bad_file.edi"))


def test_segment_terminator(x12_files):
    with pytest.raises(
        err.SegmentTerminatorNotFoundError,
        message="Expected SegmentTerminatorNotFoundError",
    ):
        Parser((x12_files["errors"] / "segment_terminator.edi"))


def test_error_validation(x12_files):
    parser = Parser((x12_files["errors"] / "error_validation.edi"))
    report = parser.document.validate()

    assert len(report.error_list) > 0
    assert report.is_document_valid() is False


def test_bad_file_input():
    with pytest.raises(TypeError, message="Expected TypeError"):
        Parser(X12_DIR)


def test_coverage(x12_files):
    parser = Parser((x12_files["errors"] / "unknown_segment_error.edi"))
    repr(parser.document)
    str(parser.document.interchange.header)
