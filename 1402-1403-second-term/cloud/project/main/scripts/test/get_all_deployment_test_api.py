import requests
import json

url = 'http://91.107.243.67:5000/get_all_deps'

response = requests.post(url)

print(response.text)

