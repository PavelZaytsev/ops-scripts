FROM openjdk:8-jdk-alpine3.8

WORKDIR /app


ADD config.yaml /app/config.yaml
ADD jmx_prometheus_httpserver-0.11.0-jar-with-dependencies.jar /app/jmx_prometheus_httpserver-0.11.0-jar-with-dependencies.jar
ADD run.sh /app/run.sh

CMD ./run.sh
