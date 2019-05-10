#!/usr/bin/env bash

set -e -x

if [ $1 = "up" ]; then
  kubectl apply -f es/elasticsearch.yaml || true # elasticsearch
  helm install stable/prometheus --name prometheus -f prometheus/values.yaml || true # prometheus
  kubectl apply -f kibana/kibana.yaml || true # kibana
  kubectl apply -f fluent-bit/fluent-bit-daemonset-elasticsearch.yaml || true # fluent-bit
  helm install --name jaeger stable/jaeger-operator || true # jaeger operator
  sleep 5
  kubectl apply -f jaeger/jaeger.yaml # jaeger
elif [ $1 = "down" ]; then
  kubectl delete -f es/elasticsearch.yaml || true # elasticsearch
  helm delete prometheus --purge || true # prometheus
  kubectl delete -f kibana/kibana.yaml || true # kibana
  kubectl delete -f fluent-bit/fluent-bit-daemonset-elasticsearch.yaml || true # fluent-bit
  kubectl delete -f corfu/corfu.yaml || true # corfu
  kubectl delete -f corfu/corfu-exporter.yaml || true # corfu exporter
  helm delete jaeger --purge || true # jaeger-operator
  kubectl delete -f jaeger/jaeger.yaml || true # jaeger
else
  echo "Unknown command"
  exit 1
fi
