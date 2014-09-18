#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

URL="http://biosual.cbio.uct.ac.za/solr/admin/cores?action=UNLOAD\&deleteIndex=true\&core="

echo "curl "${URL}$1
