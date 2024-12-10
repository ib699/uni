#!/usr/bin/env bash

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm package kaas-api
helm install kaas-api-release ./kaas-api-0.1.0.tgz


# delete 
# helm delete kaas-api-release  -n default
