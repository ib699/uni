#!/usr/bin/env bash

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# install prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus-operator prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace

# install grafana
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana grafana/grafana


# user 'admin' password 
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# expose grafana
# export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
    #  kubectl --namespace default port-forward $POD_NAME 3000


