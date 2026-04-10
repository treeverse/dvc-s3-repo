#!/bin/bash

if [ "$1" != "rpm" ] && [ "$1" != "deb" ]; then
  echo "Usage: ${0##*/} {deb|rpm}" && exit 1
fi

git config --global --add safe.directory "$(pwd)/dvc"

uv pip install './dvc[all]' -r ./build-requirements.txt
python build_bin.py
python build_pkg.py "${1}"
