#!/bin/sh
set -e

KEY=$(pwd)/ppa_deadsnakes.key
DEST=$(pwd)/ppa_deadsnakes.gpg
GNUPGHOME=$(mktemp -d)
trap "{ rm -rf $GNUPGHOME; }" EXIT
export GNUPGHOME


rm -f $DEST
gpg --import $KEY
gpg --output $DEST --export
gpg --list-keys --no-default-keyring --keyring $DEST
