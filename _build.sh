#!/usr/bin/env bash

# Don't run this script directly, run github_release.sh instead

set -ex

rm debian -rf

~/venv/bin/zander

cd subfind_web/ui
yarn build

cd ../..

./deb_build.sh
./publish.sh
