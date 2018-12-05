#!/usr/bin/env bash
set -e

apt-get update && apt-get --assume-yes install curl

curl -qf "${TARGET_URL}"
