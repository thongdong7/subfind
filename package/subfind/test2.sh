#!/usr/bin/env bash

set -e

APP_DIR=/data/projects/subfind


PACKAGE=subfind
VERSION=4.5.0

export DEBEMAIL=thongdong7@gmail.com
export DEBFULLNAME="Thong Dong"

#rm -rf $PACKAGE-$VERSION
rm -rf $PACKAGE*

mkdir $PACKAGE-$VERSION
cd $PACKAGE-$VERSION

echo dh_make :: Create
dh_make --createorig --indep # this will prompt you to hit enter

mkdir essentials
mv debian/{changelog,compat,rules,control} essentials
rm -r debian
mv essentials debian

cp -rf ../files .
cp -rf $APP_DIR/subfind files/var/lib/subfind/
cp -rf $APP_DIR/subfind_cli files/var/lib/subfind/
cp -rf $APP_DIR/subfind_provider_opensubtitles files/var/lib/subfind/
cp -rf $APP_DIR/subfind_provider_subscene files/var/lib/subfind/
cp -rf $APP_DIR/subfind_web files/var/lib/subfind/

echo './files/* ./' > debian/$PACKAGE.install
python -m compileall files

#mkdir -p example-src/usr/share/example
#touch example-src/usr/share/example/file # create the empty file to be installed

echo Run dpkg-buildpackage
dpkg-buildpackage -uc -tc -rfakeroot || true

echo Run dpkg
dpkg --contents ../"$PACKAGE"_$VERSION-1_all.deb # inspect the resulting Debian package

#echo List files
#dpkg-deb -c $PACKAGE_$VERSION-1_all.deb

echo Install
dpkg -i ../"$PACKAGE"_$VERSION-1_all.deb

echo Execute
subfind

apt remove -y subfind
