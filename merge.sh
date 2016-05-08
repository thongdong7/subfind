#!/usr/bin/env bash

set -e

SRC_BRANCH=master
DESC_BRANCH=4-stable

git checkout $DESC_BRANCH
git merge $SRC_BRANCH

git pull
git push

git checkout $SRC_BRANCH
