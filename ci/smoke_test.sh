#!/bin/sh
set -e

apk update
apk upgrade
apk add curl

curl -qf "${TARGET_URL}"
