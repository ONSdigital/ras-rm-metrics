#!/usr/bin/env bash
set -e

apt-get update
apt-get install curl

curl -qf "${TARGET_URL}"