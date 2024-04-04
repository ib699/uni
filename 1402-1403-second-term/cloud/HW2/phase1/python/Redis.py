import redis


class Redis:
    def __init__(self):
        try:
            self.r = redis.Redis(host='192.168.249.4', port=6379, db=0)
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

# test = Redis()
# print(test.search("test"))
# print(test.insert("test","go"))
