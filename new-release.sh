#!/bin/bash

VERSION=$1
if [ "$VERSION" == "" ]; then
    echo Bitte version angeben
    exit
fi
sed -e "s/VERSION = \".*\"\$/VERSION = \"$VERSION\"/" tour2pdf_mod/const.py
git commit -m "Neue Version $VERSION" tour2pdf_mod/const.py
git tag v$VERSION
git push origin v$VERSION
git push origin main
