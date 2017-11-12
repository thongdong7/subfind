#!/usr/bin/env bash

set -ex

rm debian -rf

~/venv/bin/zander

cd subfind_web/ui
yarn build

cd ../..

./deb_build.sh
