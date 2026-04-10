#!/bin/bash

set -e

if [ -z "$AWS_S3_BUCKET" ]; then
  echo "AWS_S3_BUCKET is not set."
  exit 1
fi

if [ -z "$AWS_S3_PREFIX" ]; then
  echo "AWS_S3_PREFIX is not set."
  exit 1
fi

DIR=$(dirname "${BASH_SOURCE[0]}")
PKG="../*.rpm"
RPM_REPO=$DIR/dvc.repo
ASC=$DIR/../iterative.asc
RPM_S3_DIR=$DIR/rpm-s3

printenv GPG_ITERATIVE_PASS > ~/iterative.pass
cp $DIR/rpmmacros ~/.rpmmacros

aws s3 cp $RPM_REPO s3://$AWS_S3_BUCKET/$AWS_S3_PREFIX/
aws s3 cp $ASC s3://$AWS_S3_BUCKET/$AWS_S3_PREFIX/
aws s3 cp $ASC s3://$AWS_S3_BUCKET/$AWS_S3_PREFIX/gpg/

printenv GPG_ITERATIVE_ASC > Iterative.secret.asc
gpg2 --no-tty --batch --passphrase-file ~/iterative.pass --pinentry-mode loopback --import Iterative.secret.asc

rm -rf $RPM_S3_DIR
git clone https://github.com/iterative/rpm-s3 $RPM_S3_DIR --recurse-submodules

rpm --resign $PKG

export AWS_ACCESS_KEY=$(printenv AWS_ACCESS_KEY_ID)
export AWS_SECRET_KEY=$(printenv AWS_SECRET_ACCESS_KEY)
$RPM_S3_DIR/bin/rpm-s3 -vvv \
  --bucket $AWS_S3_BUCKET \
  --repopath $AWS_S3_PREFIX \
  --region $(printenv AWS_DEFAULT_REGION) \
  --keep 100 \
  --visibility None \
  --sign \
  --gpg-bin gpg2 \
  --gpg-options="--no-tty --batch --passphrase-file ~/iterative.pass  --pinentry-mode loopback" \
  $PKG

cp $RPM_REPO /etc/yum.repos.d/
rpm --import $ASC
dnf update --verbose
dnf install -y dvc
