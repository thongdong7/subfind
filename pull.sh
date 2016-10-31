#!/usr/bin/env bash

set -e

function pull() {
  if [ ! -d $1 ]; then
    echo $1 not exists
  else
    echo Pull $1...
    cd $1
    git pull
    cd ..
  fi

}

cd ..
pull subfind
pull tb-react
pull tb-api
pull tb-ioc
pull code-gen
