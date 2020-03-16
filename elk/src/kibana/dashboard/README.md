## Corfu Log Aggregation Platform Dashboards

curl --user elastic:changeme -X POST "localhost:5601/api/kibana/dashboards/import?exclude=index-pattern" -H 'kbn-xsrf: true' -H 'Content-Type: application/json'

- saving queries https://www.elastic.co/blog/reusing-saved-queries-in-kibana-across-dashboard-visualize-and-discover

find objects in kibana https://www.elastic.co/guide/en/kibana/master/saved-objects-api-find.html

find an index curl -u elastic:changeme -X GET "localhost:5601/api/saved_objects/_find?type=index-pattern&search_fields=title&search=bug123" -H 'kbn-xsrf: true' > x.json

import dashboard
curl -u elastic:changeme -X POST "localhost:5601/api/kibana/dashboards/import?exclude=index-pattern" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d @src/kibana/dashboard/dashborda.json

export dashboard:
curl --user elastic:changeme -X GET "localhost:5601/api/kibana/dashboards/export?dashboard=23fb4430-6304-11ea-8b40-23c86bfce2b5" -H 'kbn-xsrf: true'

------------------
RabbitMq logs 
 - https://www.elastic.co/guide/en/beats/filebeat/master/filebeat-module-rabbitmq.html
 - https://logz.io/blog/monitoring-rabbitmq-with-elk-and-logz-io-part-1/
 
Java GC monitoring
 - https://bit.ly/2v1FdWv - request
 
 - https://logz.io/blog/java-garbage-collection/
 - https://github.com/Mortinke/logstash-pattern
 
Checkpointer
 - https://gitlab.eng.vmware.com/aanmol/support-bundle-helper
  