import json
from typing import Any, Optional
from app.core.redisClient import redisClient, checkRedisConnection


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
        if redisClient is None:
            return

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
        if redisClient is None:
            return None

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
        if redisClient is None:
            return

        redisClient.delete(self._formatKey(namespace, key))

    # -------------------------
    # HEALTH CHECK
    # -------------------------
    def health(self) -> bool:
        return checkRedisConnection()


cacheService = CacheService()