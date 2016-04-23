#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

set -e

echo Upload subfind
cd $DIR/../subfind
python setup.py bdist_wheel --universal upload

echo Upload opensubtitles
cd $DIR/../subfind-provider-opensubtitles
python setup.py bdist_wheel --universal upload

echo Upload subscene
cd $DIR/../subfind-provider-subscene
python setup.py bdist_wheel --universal upload

echo Upload cli
cd $DIR/../subfind-cli
python setup.py bdist_wheel --universal upload
