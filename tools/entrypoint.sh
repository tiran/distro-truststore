#!/bin/sh
set -x

PYTHON="${PYTHON:-python3}"
DISTRO_TRUSTSTORE_NAME="${DISTRO_TRUSTSTORE_NAME:-unknown}"

export DISTRO_TRUSTSTORE_NAME

${PYTHON} /check_openssl_conf.py
