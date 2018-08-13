#!/usr/bin/env python
from setuptools import setup, find_packages

from badX12.__project__ import author, author_email, version, homepage


def fread(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='badX12',
    version=version,

    author=author,
    author_email=author_email,
    url=homepage,
    packages=find_packages(exclude=('tests', 'docs')),
    description=(
        'A Python API for parsing ANSI ASC X12 files.'
    ),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    long_description=fread('README.rst'),
    license=fread('LICENSE'),

    install_requires=[
    ],

    project_urls={
        'Bug Tracker': f'{homepage}/issues',
        'Documentation': f'{homepage}/tree/master/docs',
        'Source Code': f'{homepage}',
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='x12 edi parser'
)
