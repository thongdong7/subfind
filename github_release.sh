#!/usr/bin/env bash

set -ex

GH_USER=thongdong7
GH_PATH=$GITHUB_TOKEN
GH_REPO=subfind
GH_TARGET=master
ASSETS_PATH=`pwd`/..

VERSION=`./get_version.py`

echo Build...
./build.sh

echo Create tag...
git tag $VERSION
git push --tags

CODE_BLOCK="\`\`\`"


echo Create release...
res=`curl --user "$GH_USER:$GH_PATH" -X POST https://api.github.com/repos/${GH_USER}/${GH_REPO}/releases \
-d "
{
  \"login\": \"$GH_USER\",
  \"token\": \"$GITHUB_TOKEN\",
  \"tag_name\": \"$VERSION\",
  \"target_commitish\": \"$GH_TARGET\",
  \"name\": \"$VERSION\",
  \"body\": \"Install:\n\n${CODE_BLOCK}bash\n$ sudo dpkg -i subfind_$VERSION-1_all.deb\n$ sudo service subfind restart\n${CODE_BLOCK}\",
  \"draft\": false,
  \"prerelease\": false
}"`
echo Create release result: ${res}
rel_id=`echo ${res} | python -c 'import json,sys;print(json.load(sys.stdin)["id"])'`
file_name=subfind_${VERSION}-1_all.deb

echo Upload files....
curl --user "$GH_USER:$GH_PATH" -X POST https://uploads.github.com/repos/${GH_USER}/${GH_REPO}/releases/${rel_id}/assets?name=${file_name}\
 --header 'Content-Type: text/javascript ' --upload-file ${ASSETS_PATH}/${file_name}

