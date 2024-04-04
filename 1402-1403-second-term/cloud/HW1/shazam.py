import requests

def getSongName(file_name):
	try:
		print("sterted shazam")
		url = "https://shazam-api-free.p.rapidapi.com/shazam/recognize/"

		files = { "upload_file": open(file_name, 'rb') }
		headers = {
		"X-RapidAPI-Key": "9ba65105cfmshde1366229527dcap11047ajsn905d72f2773a",
		"X-RapidAPI-Host": "shazam-api-free.p.rapidapi.com"
		}

		response = requests.post(url, files=files, headers=headers)

		print("ended shazam")
		return response.json()['track']['title']
	except Exception as e:
		return False