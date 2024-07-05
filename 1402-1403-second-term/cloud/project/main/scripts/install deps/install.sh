#!/usr/bin/env bash

update(){
sudo apt update
sudo apt upgrade
}

install_deps(){
	if ! command -v docker &> /dev/null
	then
		for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
		# Add Docker's official GPG key:
		sudo apt-get update
		sudo apt-get install ca-certificates curl
		sudo install -m 0755 -d /etc/apt/keyrings
		sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
		sudo chmod a+r /etc/apt/keyrings/docker.asc
		
		# Add the repository to Apt sources:
		echo \
		  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
		  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
		  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
		sudo apt-get update
		sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
	fi
	

	if ! command -v k3s &> /dev/null
	then
		curl -sfL https://get.k3s.io | sh -
		sudo k3s kubectl get node
	fi	

	
	if ! command -v helm &> /dev/null
	then
		curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
		chmod 700 get_helm.sh
		./get_helm.sh
	
	fi
	
	helm version
	check=$(helm repo list 2>&1)

	if [[ $check == *"Error: no repositories to show"* ]]; then
		helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
		helm repo update
		export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
		helm install nginx-ingress ingress-nginx/ingress-nginx
	fi

	kubectl get pods --namespace default -l app.kubernetes.io/name=ingress-nginx


	sudo apt install python3
	sudo apt install pip
	pip install -r requirements.txt --break-system-packages
}

update
install_deps
