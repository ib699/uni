#!/bin/bash

read -p "1) status 2) reset all 3) create all  " input

if [ $input -eq 1 ]; then
	# get data status
	echo "//-- pods: --//"
	kubectl get pods
	echo "//-- services: --//"
	kubectl get services
	echo "//-- deployment: --//"
	kubectl get deployment
	echo "//-- pvc: --//"
	kubectl get pvc
	echo "//-- pv: --//"
	kubectl get pv
elif [ $input -eq 2 ]; then

	read -p "deleting all are you sure? (y)N   " sure
	if [ $sure == "y" ]; then
		echo "deleting all deployment & services"	
		kubectl delete service python-app-service
		kubectl delete service elasticsearch
		kubectl delete service redis 
		kubectl delete deployment elasticsearch-deployment
		kubectl delete deployment redis-deployment 
		kubectl delete deployment python-app-deployment
	fi

	read -p "deleting disks are you sure? (y)N   " disk
	if [ $disk == "y" ]; then
		kubectl delete pv my-pv
		kubectl delete pvc my-pvc
	fi	

elif  [ $input -eq 3 ]; then
	# create configs
	kubectl apply -f .
else 
	echo "Wrong Input"
fi
