#!/usr/bin/env bash

npm run dist

python setup.py bdist_wheel --universal upload
