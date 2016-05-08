#!/usr/bin/env bash

set -e

chmod +x subfind/usr/bin/subfind

echo remove deb file
rm -f subfind.deb

echo compile
#dpkg -b subfind
debuild --no-tgz-check

echo install
sudo dpkg -i subfind.deb

echo validate subfind file
ls -la /usr/bin/|grep subfind

if [ ! -e /usr/bin/subfind ]; then
  echo Subfind is not installed
fi

