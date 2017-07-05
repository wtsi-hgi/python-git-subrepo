#!/usr/bin/env bash
set -eu -o pipefail

PYTHONPATH=. coverage run -m unittest discover -v -s gitsubrepo/tests
coverage run setup.py install
coverage combine -a
coverage report
