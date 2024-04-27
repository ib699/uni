#!/bin/bash

# phase 1
docker-compose up -d

# phase 3
docker build -t my-python-app .
docker tag my-python-app isedighi/cloud
docker push isedighi/cloud
