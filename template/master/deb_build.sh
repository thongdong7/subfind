#!/usr/bin/env bash

{{ generated_file_note }}

set -e

PACKAGE={{package}}
VERSION={{version}}

rm ../{{package}}_{{version}}-1_amd64.deb || true

dpkg-buildpackage -us -uc

sudo apt-get remove -y {{package}} || true
sudo dpkg -i ../{{package}}_{{version}}-1_amd64.deb

test -x /opt/venvs/{{package}}/bin/{{PackageService}}
/opt/venvs/{{package}}/bin/pip list

echo Expect service script exists
test -x /lib/systemd/system/{{package}}.service

echo Done
