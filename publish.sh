#!/usr/bin/env bash

set -e

rm subfind_web/static/js/* -rf

echo Build js files...
npm run dist

echo Upload packages...
python setup.py bdist_wheel --universal upload
