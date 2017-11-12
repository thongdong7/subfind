#!/usr/bin/env bash

set -ex

rm debian -rf

~/venv/bin/zander

./deb_build.sh
