#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
export PYTHONPATH=$DIR

./env/bin/python subfind_web/app.py
