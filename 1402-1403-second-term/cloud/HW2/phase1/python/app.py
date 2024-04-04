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

    re_resp = re.search(search_query)
    if re_resp is not None:
        print("-- found in redis search --")
        return re_resp

    es_resp = es.search(search_query)
    if es_resp is not None:
        print("-- found in elastic search --")
        re.insert(search_query, str(es_resp))
        return es_resp

    api_resp = api.search(search_query)
    if api_resp is not None:
        print("-- found api search --")
        re.insert(search_query, str(api_resp))
        return api_resp

    return print("-- found Nothing! --")


if __name__ == '__main__':
    app.run()
