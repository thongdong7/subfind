#!/usr/bin/env bash

set -e

echo Build js files...
npm run dist

echo Upload packages...
python setup.py bdist_wheel --universal upload
