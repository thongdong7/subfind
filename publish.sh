#!/usr/bin/env bash

set -e

rm subfind_web/static/js/* -rf

echo Build js files...
npm run dist

echo Upload packages...
python setup.py bdist_wheel --universal upload

echo Build deb file
rm deb_dist -rf

python3 setup.py --command-packages=stdeb.command bdist_deb
python setup.py --command-packages=stdeb.command bdist_deb

#dpkg -i deb_dist/python3-subfind_4.5.0-1_all.deb
