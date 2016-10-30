#!/usr/bin/env bash

set -e

PACKAGE=subfind
VERSION=4.5.3

FULL_PACKAGE=$PACKAGE-$VERSION
FULL_PACKAGE2=${PACKAGE}_$VERSION
echo $FULL_PACKAGE2
rm *.tar.gz || true
rm *.deb || true

dpkg-buildpackage -us -uc

apt-get remove -y $PACKAGE || true

sudo apt-get remove -y $PACKAGE
sudo dpkg -i ../$FULL_PACKAGE2-1_amd64.deb

test -x /opt/venvs/$PACKAGE/bin/subfind-web
/opt/venvs/$PACKAGE/bin/pip list

#hello

echo Expect service script exists
test -x /etc/init.d/$PACKAGE || echo Not exists

echo Done
