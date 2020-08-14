#!/usr/bin/env bash

set -e
set -x

mypy badx12
flake8 badx12 tests
black badx12 tests --check
isort badx12 tests --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --check-only
