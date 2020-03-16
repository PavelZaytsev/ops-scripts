## Corfu Log Aggregation Platform
[Documentation](docs/corfu_lap.md)

curl -X POST "localhost:5601/api/kibana/dashboards/import?exclude=index-pattern" -H 'kbn-xsrf: true' -H 'Content-Type: application/json'

find objects in kibana https://www.elastic.co/guide/en/kibana/master/saved-objects-api-find.html

find an index curl -u elastic:changeme -X GET "localhost:5601/api/saved_objects/_find?type=index-pattern&search_fields=title&search=bug123" -H 'kbn-xsrf: true' > x.json

