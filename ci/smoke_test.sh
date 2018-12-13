#!/bin/sh
set -e

apk update
apk upgrade
#apk add bash
apk add curl
#apt-get --assume-yes update && apt-get --assume-yes install curl

curl -qf "${TARGET_URL}"
