#!/usr/bin/env bash


read -p "1)status 2)delete	" ans

if [ $ans == "2" ]; then
	kubectl delete svc example-app
	kubectl delete secret secret1
	kubectl delete deployment example-app
	kubectl delete ingress example-app
	kubectl delete secret postgresql-credentials
	kubectl delete deployment my-postgres-db
	kubectl delete svc my-postgres-db-service
else
	kubectl get svc 
	kubectl get secret 
	kubectl get deployment 
	kubectl get ingress

fi
