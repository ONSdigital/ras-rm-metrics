#!/bin/sh
set -e

apt-get --assume-yes update && apt-get --assume-yes install curl

curl -qf "${TARGET_URL}"
