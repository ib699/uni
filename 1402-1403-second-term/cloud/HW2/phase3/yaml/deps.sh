#!/bin/bash

# install k3s from https://k3s.io/
curl -sfL https://get.k3s.io | sh - 
# Check for Ready node, takes ~30 seconds 
sudo k3s kubectl get node

# install kind from https://kind.sigs.k8s.io/
wget https://golang.org/dl/go1.17.2.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.17.2.linux-amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
" >> ~/.bashrc
source ~/.profile
go install sigs.k8s.io/kind@v0.22.0
echo 'export PATH="/home/lwall/go/bin/:$PATH"' >> ~/.bashrc

# install rancher from https://github.com/rancher/rancher?tab=readme-ov-file 
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce
sudo systemctl start docker
sudo systemctl enable docker
docker --version
sudo docker run -d --restart=unless-stopped -p 80:80 -p 443:443 --privileged rancher/rancher
docker pull rancher/shell:v0.1.22

# install minikube from https://minikube.sigs.k8s.io/docs/start/
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

mkdir /root/Documents/redis
