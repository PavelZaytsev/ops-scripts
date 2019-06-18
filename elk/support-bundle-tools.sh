#!/usr/bin/env bash

docker run -ti \
-v $(pwd)/src/prepare_logs.py:/prepare_logs.py \
-v $(pwd)/build/data/$1:/bug/data/$1 \
-v $(pwd)/build/docker-elk/data:/output/data/ \
--workdir=/bug \
pypy:3-7.0 sh -c "/usr/local/bin/pypy3 /prepare_logs.py $1"
