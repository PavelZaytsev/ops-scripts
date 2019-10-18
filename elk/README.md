# ELK

Prepare logs for stashing:

${bundle_name} - tar file which contains support bundles.

0. Run `./init.sh`
1. Put the bundle in the build/data directory (the tar file name will be the index name in elk) 
2. Run `./support-bundle-tools.sh <bundle_name>`.
3. Run `elk-up.sh`

#New functionality
Download a tgz support bundle into data directory
./gradlew processing -Pbug=my_bug -Purl=http://url.com/123.tgz -Pbundle=123

### Unpack support bundle
./gradlew unpack -Pbug=my_bag -Pbundle=1.tgz
./support-bundle-tools.sh
./elk-up.sh
