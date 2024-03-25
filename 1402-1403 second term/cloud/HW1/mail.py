import requests


def send_mail(to, text):
    url = "https://send-mail-serverless.p.rapidapi.com/send"

    payload = {
        "personalizations": [{"to": [
            {
                "email": f"{to}",
                "name": "Recipient name"
            }
        ]}],
        "from": {
            "email": "test@firebese.com",
            "name": "Firebese Test Use"
        },
        "reply_to": {
            "email": "test@firebese.com",
            "name": "Firebese Test User"
        },
        "subject": "Example subject",
        "content": [
            {
                "type": "text/html",
                "value": f"{text}  <b>Html</b>"
            },
            {
                "type": "text/plan",
                "value": text
            }
        ],
        "headers": {
            "List-Unsubscribe": "<mailto: unsubscribe@firebese.com?subject=unsubscribe>, <https://firebese.com/unsubscribe/id>"}
    }
    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "9ba65105cfmshde1366229527dcap11047ajsn905d72f2773a",
        "X-RapidAPI-Host": "send-mail-serverless.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
