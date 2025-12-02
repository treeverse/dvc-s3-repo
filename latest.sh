#!/bin/sh

set -e

PROJECT="treeverse/dvc"
echo $(gh release list -R $PROJECT -L1 | awk -F '\t' '{ print $3 }')
