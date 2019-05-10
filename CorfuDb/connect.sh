#!/bin/sh
set -e -x

if [ $1 = "kill" ]; then
  kill $(lsof -t -i :8001)
  kill $(lsof -t -i :5601)
  kill $(lsof -t -i :9090)
  kill $(lsof -t -i :16686)
elif [ $1 = "forward" ]; then
  kubectl proxy &
  kubectl port-forward $(kubectl get pods --no-headers -o=name -l k8s-app=kibana-logging) 5601 &
  kubectl port-forward $(kubectl get pods --no-headers -o=name -l app=prometheus) 9090 &
  kubectl port-forward $(kubectl get pods --no-headers -o=name -l app=jaeger | grep jaeger-query) 16686 &
else
  echo "Unknown command"
  exit 1
fi
