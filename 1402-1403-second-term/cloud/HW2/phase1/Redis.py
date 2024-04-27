import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()

pv_file = '/root/Documents/redis/redis_data.json'


class Redis:
    def __init__(self):
        ip = os.getenv('REDIS_IP')
        port = os.getenv('REDIS_PORT')
        try:
            self.r = redis.Redis(host='redis', port=6379, db=0)
        except Exception as e:
            print("could not connect to redis")

    def search(self, key):
        print("-- started redis search --")
        value = self.r.get(key)
        return value

    def insert(self, key, value):
        resp = self.r.set(key, value)
        return resp

    def delete(self, key):
        self.r.delete(key)

    def import_data(self):
        with open(pv_file, 'r') as file:
            imported_data = json.load(file)

        # Insert data back into Redis
        for key, value in imported_data.items():
            self.r.set(key, value)

    def export_data(self):
        keys = self.r.keys('*')

        data = {}
        for key in keys:
            data[key.decode()] = self.r.get(key).decode()

        with open(pv_file, 'w') as file:
            json.dump(data, file)

# test = Redis()
# print(test.search("test"))
# print(test.insert("test","go"))
