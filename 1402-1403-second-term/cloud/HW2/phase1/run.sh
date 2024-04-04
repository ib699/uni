#!/bin/bash

docker pull redis:alpine3.19
docker pull elasticsearch:8.12.2


docker-compose up -d

# run elastic search
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "ELASTIC_PASSWORD=12345" -m 2g --name my_elasticsearch elasticsearch:8.12.2

# run redis
docker run -d -p 6379:6379 --name my-redis-container redis:alpine3.19
