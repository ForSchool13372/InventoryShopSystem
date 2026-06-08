from app.core.cacheService import CacheService


class FakeRedis:
    def __init__(self):
        self.store = {}
        self.lastSetex = None
        self.deletedKey = None

    def set(self, key, value):
        self.store[key] = value

    def setex(self, key, ttl, value):
        self.lastSetex = (key, ttl, value)
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)

    def delete(self, key):
        self.deletedKey = key
        self.store.pop(key, None)

    def ping(self):
        return True


def test_format_key():
    cache = CacheService()

    assert cache._formatKey("player", "1") == "player:1"


def test_set_without_ttl(monkeypatch):
    fakeRedis = FakeRedis()

    monkeypatch.setattr(
        "app.core.cacheService.redisClient",
        fakeRedis,
    )

    cache = CacheService()

    cache.set("player", "1", {"gold": 100})

    assert "player:1" in fakeRedis.store


def test_set_with_ttl(monkeypatch):
    fakeRedis = FakeRedis()

    monkeypatch.setattr(
        "app.core.cacheService.redisClient",
        fakeRedis,
    )

    cache = CacheService()

    cache.set("player", "1", {"gold": 100}, ttl=60)

    assert fakeRedis.lastSetex is not None
    assert fakeRedis.lastSetex[0] == "player:1"
    assert fakeRedis.lastSetex[1] == 60


def test_get_returns_deserialized_json(monkeypatch):
    fakeRedis = FakeRedis()
    fakeRedis.store["player:1"] = '{"gold": 100}'

    monkeypatch.setattr(
        "app.core.cacheService.redisClient",
        fakeRedis,
    )

    cache = CacheService()

    result = cache.get("player", "1")

    assert result == {"gold": 100}


def test_get_returns_none_when_missing(monkeypatch):
    fakeRedis = FakeRedis()

    monkeypatch.setattr(
        "app.core.cacheService.redisClient",
        fakeRedis,
    )

    cache = CacheService()

    assert cache.get("player", "999") is None


def test_get_returns_raw_value_when_json_invalid(monkeypatch):
    fakeRedis = FakeRedis()
    fakeRedis.store["player:1"] = "plain-text"

    monkeypatch.setattr(
        "app.core.cacheService.redisClient",
        fakeRedis,
    )

    cache = CacheService()

    assert cache.get("player", "1") == "plain-text"


def test_delete_removes_key(monkeypatch):
    fakeRedis = FakeRedis()

    monkeypatch.setattr(
        "app.core.cacheService.redisClient",
        fakeRedis,
    )

    cache = CacheService()

    cache.delete("player", "1")

    assert fakeRedis.deletedKey == "player:1"


def test_health_returns_ping_result(monkeypatch):
    fakeRedis = FakeRedis()

    monkeypatch.setattr(
        "app.core.cacheService.redisClient",
        fakeRedis,
    )

    cache = CacheService()

    assert cache.health() is True