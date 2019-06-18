#!/usr/bin/env bash

docker run -ti \
-v $(pwd)/src/prepare_logs.py:/prepare_logs.py \
-v $(pwd)/build/data/$1:/bug/data/$1 \
-v $(pwd)/build/docker-elk/data:/bug/data/ \
--workdir=/bug \
python:3.7.3-stretch sh -c "/usr/local/bin/python /prepare_logs.py $1"
