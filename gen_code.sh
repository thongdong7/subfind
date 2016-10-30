#!/usr/bin/env bash

echo "Monitoring gen folder"

find template |entr sh -c "~/dev3/bin/code-gen"
