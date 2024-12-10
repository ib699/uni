#!/bin/bash

read -p "1)Run or 2)BUlid" input

if [ $input -eq 2 ]; then
    docker build -t my-python-app .
elif [ $input -eq 1 ]; then 
    docker run my-python-app
else 
    docker tag my-python-app isedighi/cloud
    docker push isedighi/cloud
fi

