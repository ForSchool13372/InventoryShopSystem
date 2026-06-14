from fastapi import Depends
from app.core.deps import getCurrentGame
from app.core.redisClient import redisClient


def rateLimiter(action: str, limit: int = 5, window: int = 1):
    def dependency(game=Depends(getCurrentGame)):

        # Redis not ready (tests / startup safety)
        if redisClient is None:
            return True

        key = f"ratelimit:{action}:{game.playerId}"
        count = redisClient.incr(key)

        if count == 1:
            redisClient.expire(key, window)

        return count <= limit

    return dependency