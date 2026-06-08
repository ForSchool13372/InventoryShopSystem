import pytest
from fastapi import HTTPException

from app.api.routes.cacheRoutes import health, setCache, getCache
from app.core.cacheService import cacheService


class FakeCache:
    def __init__(self):
        self.store = {}

    def health(self):
        return True

    def set(self, namespace, key, value, ttl):
        self.store[(namespace, key)] = (value, ttl)

    def get(self, namespace, key):
        return self.store.get((namespace, key), (None, None))[0]


def test_health_returns_success(monkeypatch):
    monkeypatch.setattr(cacheService, "health", lambda: True)

    result = health()

    assert result == {"success": True}


def test_set_cache_success(monkeypatch):
    fake = FakeCache()

    monkeypatch.setattr("app.api.routes.cacheRoutes.cacheService", fake)

    payload = type("obj", (), {
        "namespace": "player",
        "key": "1",
        "value": {"gold": 100},
        "ttl": 60
    })

    result = setCache(payload)

    assert result == {"success": True}
    assert fake.store[("player", "1")][0] == {"gold": 100}


def test_get_cache_hit(monkeypatch):
    fake = FakeCache()
    fake.store[("player", "1")] = ({"gold": 100}, 60)

    monkeypatch.setattr("app.api.routes.cacheRoutes.cacheService", fake)

    result = getCache("player", "1")

    assert result["success"] is True
    assert result["cached"] is True
    assert result["data"] == {"gold": 100}


def test_get_cache_miss(monkeypatch):
    fake = FakeCache()

    monkeypatch.setattr("app.api.routes.cacheRoutes.cacheService", fake)

    result = getCache("player", "999")

    assert result["success"] is True
    assert result["cached"] is False
    assert result["data"] is None