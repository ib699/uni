import requests
import json

# Define the URL for the API endpoint
url = 'http://91.107.243.67:5000/create'

# Define the JSON data to be sent in the request
data = {
    "app_name": "example-app",
    "replicas": 3,
    "image_address": "nginx",
    "image_tag": "latest",
    "domain_address": "local.example.com",
    "service_port": 80,
    "resources": {
        "limits": {"cpu": "500m", "memory": "512Mi"},
        "requests": {"cpu": "250m", "memory": "256Mi"}
    },
    "envs": {
        "ENVVAR1": "value1",
        "ENVVAR2": "value2"
    },
    "secrets": {
        "secret1": "valsecret1"
    },
    "external_access": True,
    "min_replicas": 2,
    "max_replicas": 10,
    "target_cpu_utilization_percentage": 50
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response from the server
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.json())

