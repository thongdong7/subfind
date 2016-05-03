#!/usr/bin/env bash

if [ -z $1 ]; then
  echo "Please provide tag name (e.g: 4.2.0)"
  exit 1
fi

echo Tag name: $1

git tag $1

git push origin $1
