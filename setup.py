#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["click==7.0", "dicttoxml==1.7.4"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "click==7.0"]

setup(
    author="Alberto J. Marin",
    author_email="alberto@ajmar.in",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="A Python Library for parsing ANSI ASC X12 files.",
    entry_points={"console_scripts": ["badx12=badx12.__main__:cli"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="badx12 edi x12 parser",
    name="badx12",
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/git-albertomarin/badx12",
    version="0.2.2",
    zip_safe=False,
)
