#!/usr/bin/env bash

set -e
set -x

pytest --cov=badX12 --cov=tests --cov-report=term-missing ${@}
