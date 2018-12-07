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

Installing
----------

Install and update using pip:

.. code-block:: text

    pip install -U badX12

A Simple Example
----------------

badX12 can be imported and used within your own project like so.

.. code-block:: python

    from badx12 import Parser

    parser = Parser()
    document = parser.parse_document("path-to-file/file.edi")


badX12 can also be used to parse an edi file into JSON or XML via the command line.

.. code-block:: bash

    badx12 parse "path-to-edi-file"
    badx12 parse "path-to-edi-file" -e XML -o "path-to-output-dir"

By default the parse command will output a JSON file to the current user's Documents\\badX12 directory.
The -e flag can be used to specify the export format, and the -o flag can be used to specify the output directory.

Features
--------

* Parse x12 file format into a python object
* Parse x12 file format into JSON and XML

Links
-----

* License: https://en.wikipedia.org/wiki/MIT_License
* Documentation: https://badX12.readthedocs.io.
* X12 EDI Standard: http://www.x12.org/x12-work-products/x12-edi-standards.cfm
