# -*- coding: utf-8 -*-

"""Top-level package for badX12."""
from .document import EDIDocument
from .parser import Parser
from .__main__ import cli

__author__ = """Alberto J. Marin"""
__email__ = "alberto@ajmar.in"
__version__ = "0.2.2"

__all__ = ["Parser", "EDIDocument", "cli"]
