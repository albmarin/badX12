# badX12

[![PyPi](https://img.shields.io/pypi/v/badX12.svg)](https://pypi.python.org/pypi/badX12)
[![Coverage](https://codecov.io/gh/albmarin/badX12/branch/master/graph/badge.svg)](https://codecov.io/gh/albmarin/badX12)
[![Build Status](https://img.shields.io/travis/albmarin/badX12.svg)](https://travis-ci.org/albmarin/badX12)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://en.wikipedia.org/wiki/MIT_License)


A Python Library for parsing ANSI ASC X12 files.

## Installing

Install and update using pip:

```bash
pip install -U badX12
```

## A Simple Example

badX12 can be imported and used within your own project like so.

```python
from badx12 import Parser

parser = Parser()
document = parser.parse_document("path-to-file/file.edi")
```


badX12 can also be used to parse an edi file into JSON or XML via the command line.

```bash
badx12 parse "path-to-edi-file"
badx12 parse "path-to-edi-file" -e XML -o "path-to-output-dir"
```

By default the parse command will output a JSON file to the current user's Documents\\badX12 directory.
The -e flag can be used to specify the export format, and the -o flag can be used to specify the output directory.

## Features

* Parse x12 file format into a python object
* Parse x12 file format into JSON and XML

## Links

* License: [MIT License](https://en.wikipedia.org/wiki/MIT_License)
* Documentation: [https://badX12.readthedocs.io](https://badX12.readthedocs.io)
* X12 EDI Standard: [https://x12.org/about/about-x12](https://x12.org/about/about-x12)
