#!/usr/bin/env bash
curl -H 'Content-Type: application/json' -X PUT -d '{ "index.blocks.read_only_allow_delete": null}' localhost:9200/jrnl/_settings

curl -X GET "localhost:9200/jrnl/_settings"
