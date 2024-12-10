import requests


def get_song_id(song_name):
    print("sterted spotify search")
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q": f"{song_name}", "type": "tracks", "offset": "0", "limit": "1", "numberOfTopResults": "5"}

    headers = {
        "X-RapidAPI-Key": "9ba65105cfmshde1366229527dcap11047ajsn905d72f2773a",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    data = response.json()

    id_value = data['tracks']['items'][0]['data']['id']

    print(f" value is {id_value} ")
    print("ended spotify search")
    return id_value


def get_recommended(song_id):
    url = "https://spotify23.p.rapidapi.com/recommendations/"

    querystring = {"limit": "10", "seed_tracks": f"{song_id}"}

    headers = {
        "X-RapidAPI-Key": "9ba65105cfmshde1366229527dcap11047ajsn905d72f2773a",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    data = response.json()

    name_list = []
    for key in data["tracks"]:
        print(f'data is {key["name"]}')
        name_list.append(key["name"])
    return name_list

# getSongId("star wars main theme")
# getRecommended("7a9UUo3zfID7Ik2fTQjRLi")
