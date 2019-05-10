#!/usr/bin/env bash

kubectl delete -f es/elasticsearch.yaml # elasticsearch
helm delete prometheus --purge # prometheus
helm delete jaeger --purge # jaeger-operator
kubectl delete -f jaeger/jaeger.yaml # jaeger
kubectl delete -f kibana/kibana.yaml # kibana
kubectl delete -f fluent-bit/fluent-bit-daemonset-elasticsearch.yaml # fluent-bit
kubectl delete -f jmx-exporter/exporter.yaml # corfu metrics prometheus exporter
kubectl delete -f corfu/corfu.yaml # corfu
