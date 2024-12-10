import requests
import json

# Define the URL for the API endpoint
url = 'http://91.107.243.67:5000/deploy-postgresql'

# Sample data for PostgreSQL deployment
data = {
    "AppName": "my-postgres-db",
    "Resources": {
        "cpu": "500m",
        "memory": "1Gi"
    },
    "External": True
}

# Send the POST request
try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Deployment successful!")
    else:
        print(f"Failed to deploy PostgreSQL. Status code: {response.status_code}")
        print(response.text)
except requests.exceptions.RequestException as e:
    print(f"Error sending request: {e}")
