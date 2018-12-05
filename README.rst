======
badX12
======


.. image:: https://img.shields.io/pypi/v/badX12.svg
        :target: https://pypi.python.org/pypi/badX12

.. image:: https://codecov.io/gh/git-albertomarin/badX12/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/git-albertomarin/badX12

.. image:: https://img.shields.io/travis/git-albertomarin/badX12.svg
        :target: https://travis-ci.org/git-albertomarin/badX12

.. image:: https://readthedocs.org/projects/badx12/badge/?version=latest
        :target: https://badX12.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
        :target: https://en.wikipedia.org/wiki/MIT_License


A Python Library for parsing ANSI ASC X12 files.

A Simple Example
----------------

.. code-block:: python

    from badx12 import Parser

    parser = Parser()
    document = parser.parse_document("path-to-file/file.edi")

Features
--------

* Parse x12 file format into a python object

Links
-----

* License: https://en.wikipedia.org/wiki/MIT_License
* Documentation: https://badX12.readthedocs.io.
* X12 EDI Standard: http://www.x12.org/x12-work-products/x12-edi-standards.cfm
