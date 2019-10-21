## Corfu Log Aggregation Platform

The Corfu log aggregation platform built on top of [the ELK Stack](https://www.elastic.co/what-is/elk-stack).

**So, what is the ELK Stack?** "ELK" is the acronym for three open source projects: Elasticsearch, Logstash, and Kibana. 
- Elasticsearch is a search and analytics engine. 
- Logstash is a server‑side data processing pipeline that ingests data from multiple sources simultaneously, 
transforms it, and then sends it to a "stash" like Elasticsearch. 
- Kibana lets users visualize data with charts and graphs in Elasticsearch.

### The platform features
 - Automation tools to download, unpack and load the log data from support bundles. 
 - Log aggregation, flat log structure for the entire cluster, including corfu, mp, cpp, cbm, compactor and so on.
 - Fast requests, a query language and visualization dashboards, provide high quality user experience.
 - A scalable solution that can be extended and customized, highly automated.
 

### Demo


Prepare logs for stashing:

${bundle_name} - tar file which contains support bundles.

0. Run `./init.sh`
1. Put the bundle in the build/data directory (the tar file name will be the index name in elk) 
2. Run `./support-bundle-tools.sh <bundle_name>`.
3. Run `elk-up.sh`

#Functionality
Download a tgz support bundle into data directory
./gradlew processing -Pbug=my_bug -Purl=http://url.com/123.tgz -Pbundle=123

### Unpack support bundle
./gradlew unpack -Pbug=my_bag -Pbundle=1.tgz
./support-bundle-tools.sh
./elk-up.sh
