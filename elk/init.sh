#!/usr/bin/env bash
set -e

#download docker-elk repo into build directory
rm -rf build/docker-elk/

git clone https://github.com/deviantony/docker-elk.git build/docker-elk
cd build/docker-elk
#git checkout b000267d86655

cd ../../

docker volume rm docker-elk_elasticsearch

#copy configs into build dir
cp -R src/logstash build/docker-elk
cp -R src/docker-compose.yml build/docker-elk

mkdir build/docker-elk/elasticdata
mkdir build/docker-elk/data
mkdir -p build/data
