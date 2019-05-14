#!/usr/bin/env sh

docker run --rm -it -e XPACK_MONITORING_ENABLED=false -v `pwd`/pipeline/:/usr/share/logstash/pipeline docker.elastic.co/logstash/logstash:7.0.1
