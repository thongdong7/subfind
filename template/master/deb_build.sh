#!/usr/bin/env bash

{{ generated_file_note }}

set -e

PACKAGE={{package}}
VERSION={{version}}

FULL_PACKAGE=$PACKAGE-$VERSION
FULL_PACKAGE2=${PACKAGE}_$VERSION
echo $FULL_PACKAGE2
rm *.tar.gz || true
rm *.deb || true

dpkg-buildpackage -us -uc

apt-get remove -y $PACKAGE || true

sudo apt-get remove -y $PACKAGE
sudo dpkg -i ../$FULL_PACKAGE2-1_amd64.deb

test -x /opt/venvs/$PACKAGE/bin/{{PackageService}}
/opt/venvs/$PACKAGE/bin/pip list

echo Expect service script exists
test -x /lib/systemd/system/{{package}}.service

echo Done
