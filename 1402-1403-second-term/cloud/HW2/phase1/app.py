import time

from flask import Flask, request

import Redis
import api
import elastic

app = Flask(__name__)
re = Redis.Redis()
elastic.init_elastic()
es = elastic.Elastic()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/search')
def search():
    search_query = request.args.get('query')

    print(search_query)
    resp = []

    re_resp = re.search(search_query)
    if re_resp is not None:
        print("-- found in redis search --")
        resp.append('redis')
        resp.append(str(re_resp))
        return resp

    es_resp = es.search(search_query)
    if es_resp is not None:
        print("-- found in elastic search --")
        re.insert(search_query, str(es_resp))
        resp.append('elastic')
        resp.append(es_resp)
        return resp

    api_resp = api.search(search_query)
    if api_resp is not None:
        print("-- found api search --")
        re.insert(search_query, str(api_resp))
        resp.append('api')
        resp.append(api_resp)
        return resp

    return print("-- found Nothing! --")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)