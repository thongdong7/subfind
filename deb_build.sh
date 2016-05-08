#!/usr/bin/env bash

set -e

rm deb_dist -rf

echo Build
python3 setup.py --command-packages=stdeb.command bdist_deb

lesspipe deb_dist/python3-subfind_4.5.0-1_all.deb

#dpkg -i deb_dist/python3-subfind_4.5.0-1_all.deb
