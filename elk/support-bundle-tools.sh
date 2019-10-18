#!/usr/bin/env bash
set -e

cd build/docker-elk/data

find . -type f -name "corfu.9000*.log" -print0 | xargs -0 sed -i '' -e '/Trying connection to layout server/d'
find . -type f -name "corfu.9000*.log" -print0 | xargs -0 sed -i '' -e '/log write/d'
find . -type f -name "corfu.9000*.log" -print0 | xargs -0 sed -i '' -e '/New tail segment less than or equals to the old one/d'
