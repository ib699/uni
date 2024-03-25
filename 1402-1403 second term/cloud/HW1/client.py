import requests

url = 'http://5.75.207.167:5003/upload'
files = {'file': open('StarWars3.wav', 'rb')}
data = {'email': 'isedighi06@gmail.com'}

response = requests.post(url, files=files, data=data)

print(response.text)
