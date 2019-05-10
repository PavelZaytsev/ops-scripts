#!/usr/bin/env bash

set -e -x

if [ $1 = "up" ]; then
  kubectl apply -f es/elasticsearch.yaml # elasticsearch
  helm install stable/prometheus --name prometheus -f prometheus/values.yaml # prometheus
  helm install --name jaeger stable/jaeger-operator # jaeger operator
  kubectl apply -f jaeger/jaeger.yaml # jaeger
  kubectl apply -f kibana/kibana.yaml # kibana
  kubectl apply -f fluent-bit/fluent-bit-daemonset-elasticsearch.yaml # fluent-bit
  kubectl apply -f jmx-exporter/exporter.yaml # corfu metrics prometheus exporter
elif [ $1 = "down" ]; then
  kubectl delete -f es/elasticsearch.yaml # elasticsearch
  helm delete prometheus --purge # prometheus
  helm delete jaeger --purge # jaeger-operator
  kubectl delete -f jaeger/jaeger.yaml # jaeger
  kubectl delete -f kibana/kibana.yaml # kibana
  kubectl delete -f fluent-bit/fluent-bit-daemonset-elasticsearch.yaml # fluent-bit
  kubectl delete -f jmx-exporter/exporter.yaml # corfu metrics prometheus exporter
  kubectl delete -f corfu/corfu.yaml # corfu
else
  echo "Unknown command"
  exit 1
fi
