#!/bin/bash

testcores=`cat ../solr.xml | grep -i "testDelete" | cut -f 2 -d'"'`

echo "These test cores were found. To delete them, run the following commands individually"

for core in ${testcores}
do
URL="http://biosual.cbio.uct.ac.za/solr/admin/cores?action=UNLOAD\&deleteIndex=true\&core="${core}
echo "curl "${URL}
#curl -vv ${URL}
done

