#!/bin/bash
# basic functionality tests for dvc

set -eux

pkg=$1
if [[ $pkg == "deb" ]]; then
  dpkg -i dvc*.deb
elif [[ $pkg == "rpm" ]]; then
  rpm -i dvc*.rpm
else
  exit 1
fi

git clone https://github.com/iterative/example-get-started

pushd example-get-started
uv pip install --system -r src/requirements.txt
uv pip uninstall --system dvc

dvc doctor
dvc doctor | head -1 | grep $pkg
dvc pull
dvc repro
dvc status
