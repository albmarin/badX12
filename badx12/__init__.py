# -*- coding: utf-8 -*-

"""Top-level package for badX12."""
from .document import EDIDocument
from .parser import Parser

__author__ = """Alberto J. Marin"""
__email__ = "alberto@ajmar.in"
__version__ = "0.2.1"

__all__ = ["Parser", "EDIDocument"]
