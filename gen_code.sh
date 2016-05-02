#!/usr/bin/env bash

echo "Monitoring gen folder"

find gen |entr sh -c "export PYTHONPATH=`pwd` && ./env/bin/python gen.py"
