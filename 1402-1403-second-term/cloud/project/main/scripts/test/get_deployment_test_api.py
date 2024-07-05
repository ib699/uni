import requests
import json

url = 'http://localhost:5000/get_dep_info'

data = {
    "name": "example-app"
}

response = requests.post(url, json=data)

print(response.text)

