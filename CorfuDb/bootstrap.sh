#!/usr/bin/env bash

kubectl apply -f es/elasticsearch.yaml # elasticsearch
helm install stable/prometheus --name prometheus -f prometheus/values.yaml # prometheus
helm install --name jaeger stable/jaeger-operator # jaeger operator
kubectl apply -f jaeger/jaeger.yaml # jaeger
kubectl apply -f kibana/kibana.yaml # kibana
kubectl apply -f fluent-bit/fluent-bit-daemonset-elasticsearch.yaml # fluent-bit
kubectl apply -f jmx-exporter/exporter.yaml # corfu metrics prometheus exporter
