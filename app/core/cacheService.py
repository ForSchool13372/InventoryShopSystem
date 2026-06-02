import json
from typing import Any, Optional
from app.core.redisClient import redisClient


class CacheService:
    """
    Production-grade Redis abstraction layer
    """

    # -------------------------
    # KEY MANAGEMENT
    # -------------------------
    def _formatKey(self, namespace: str, key: str) -> str:
        return f"{namespace}:{key}"

    # -------------------------
    # SET CACHE
    # -------------------------
    def set(
        self,
        namespace: str,
        key: str,
        value: Any,
        ttl: int | None = None
    ) -> None:
        fullKey = self._formatKey(namespace, key)

        payload = json.dumps(value)

        if ttl:
            redisClient.setex(fullKey, ttl, payload)
        else:
            redisClient.set(fullKey, payload)

    # -------------------------
    # GET CACHE
    # -------------------------
    def get(
        self,
        namespace: str,
        key: str
    ) -> Optional[Any]:
        fullKey = self._formatKey(namespace, key)

        value = redisClient.get(fullKey)

        if value is None:
            return None

        try:
            return json.loads(value)
        except Exception:
            return value

    # -------------------------
    # DELETE CACHE
    # -------------------------
    def delete(self, namespace: str, key: str) -> None:
        redisClient.delete(self._formatKey(namespace, key))

    # -------------------------
    # HEALTH CHECK
    # -------------------------
    def health(self) -> bool:
        return redisClient.ping()


cacheService = CacheService()