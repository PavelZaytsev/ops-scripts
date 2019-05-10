#!/bin/sh
set -e -x

kill $(lsof -t -i :8001)
kill $(lsof -t -i :5601)
kill $(lsof -t -i :16686)
kubectl proxy &
kubectl port-forward $(kubectl get pods --no-headers -o=name -l k8s-app=kibana-logging) 5601 &
kubectl port-forward $(kubectl get pods --no-headers -o=name -l app=prometheus) 9090 &
kubectl port-forward $(kubectl get pods --no-headers -o=name -l app=jaeger) 16686 &
