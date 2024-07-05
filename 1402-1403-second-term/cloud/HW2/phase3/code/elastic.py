import time

import requests
from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch


def init_elastic():
    load_dotenv()
    url = os.getenv('ELASTIC_URL_INSERT')
    username = os.getenv('ELASTIC_USER')
    password = os.getenv('ELASTIC_PASS')

    with open("movies.json", 'r') as file:
        data = file.read()

    headers = {
        'Content-Type': 'application/json'
    }

    cont = 400
    while cont != 200:
        try:
            response = requests.post(url, auth=(username, password), headers=headers, data=data, verify=False)
            cont = response.status_code
        except Exception as e:
            print(f"Failed to index data. Waiting 10 seconds..." )
            time.sleep(10)
            continue

    print("Data successfully indexed in Elasticsearch.")


class Elastic:
    def __init__(self):
        url = os.getenv('ELASTIC_URL')
        username = os.getenv('ELASTIC_USER')
        password = os.getenv('ELASTIC_PASS')
        self.es = Elasticsearch(url, http_auth=(username, password), verify_certs=False)
        print(self.es.cluster.health())

    def search(self, query_str):
        print("-- not found in redis search --")
        print("-- started elastic search --")

        query = {
            "query": {
                "match": {
                    "Series_Title": f"{query_str}"
                }
            }
        }

        output = []

        results = self.es.search(index='your_index_name', body=query)
        for hit in results['hits']['hits']:
            output.append(hit['_source'])

        if not output:
            return None
        else:
            return output

# init_elastic()
# test = Elastic()
# print(test.search("Forrest Gumpppp"))
