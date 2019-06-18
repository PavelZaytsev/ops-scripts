#!/usr/bin/env bash

#download docker-elk repo into build directory
rm -rf build
git clone https://github.com/deviantony/docker-elk.git build/docker-elk

#copy configs into build dir
cp -R src/logstash build/docker-elk
cp -R src/docker-compose.yml build/docker-elk

mkdir build/docker-elk/elasticdata
mkdir build/docker-elk/data
mkdir build/data
