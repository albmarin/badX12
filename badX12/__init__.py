"""
    badX12
    ~~~~~~~~~~~~

    A Python API for parsing ANSI ASC X12 files.
"""
from .__project__ import version, homepage, author
from .parsers import Parser

__all__ = ['Parser']

__version__ = version
__homepage__ = homepage
__author__ = author
__license__ = 'Apache-2.0'
