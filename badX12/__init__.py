# -*- coding: utf-8 -*-

"""Top-level package for badX12."""
from .parser import Parser
from .document import EDIDocument

__author__ = """Alberto J. Marin"""
__email__ = "alberto@ajmar.in"
__version__ = "0.1.0"

__all__ = ["Parser", "EDIDocument"]
