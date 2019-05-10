#!/usr/bin/env sh
sleep 8
java -jar jmx_prometheus_httpserver-0.11.0-jar-with-dependencies.jar 8080 config.yaml
