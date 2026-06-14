class FakeRedis:
    def __init__(self):
        self.store = {}

    def set(self, key, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)

    def delete(self, key):
        return self.store.pop(key, None)

    def hset(self, name, mapping=None, **kwargs):
        self.store[name] = mapping or kwargs

    def hgetall(self, name):
        return self.store.get(name, {})

    def hincrby(self, name, key, amount):
        if name not in self.store:
            self.store[name] = {}
        self.store[name][key] = str(int(self.store[name].get(key, 0)) + amount)