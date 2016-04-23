#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHONPATH=$DIR:$DIR/../subfind:$DIR/../subfind-provider-opensubtitles:$DIR/../subfind-provider-subscene

../subfind/dev/bin/python subfind_cli/cli.py $@