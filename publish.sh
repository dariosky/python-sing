#!/usr/bin/env bash

pandoc --from=markdown --to=rst README.md -o README.rst

# to install for development: pip install -e .
rm dist/*
python setup.py sdist
twine upload dist/*
