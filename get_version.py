#!/usr/bin/env python
# encoding=utf-8

import yaml

with open('template/data/package.yml') as stream:
    data = yaml.load(stream)
    print(data['version'])
