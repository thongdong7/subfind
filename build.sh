#!/usr/bin/env bash

rm build -rf
rm dist -rf

VERSION=4.4.0
NAME=subfind-web

#  --noupx \
#  --name $NAME \
#./env/bin/pyinstaller \
#  --onefile \
#  --windowed \
#  --paths subfind:subfind_provider_opensubtitles:subfind_provider_subscene:subfind_web \
#  subfind_web/main.py

#mv dist/$NAME/$NAME dist/$NAME/$NAME.exe

nuitka --standalone --show-modules subfind_web/a.py
