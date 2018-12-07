#!/bin/bash
redisIP=$(getent hosts redis | cut -d' ' -f1)
consulIP=$(getent hosts consul | cut -d' ' -f1)
cat > json.dat <<_EOF_
{"ID": "redis", "Name": "redis", "Address": "$redisIP", "Port": 6379}
_EOF_
curl -s -X PUT -d @json.dat http://$consulIP:8500/v1/agent/service/register
rm json.dat
curl -s http://$consulIP:8500/v1/catalog/services?pretty
curl -s http://$consulIP:8500/v1/catalog/service/redis?pretty
