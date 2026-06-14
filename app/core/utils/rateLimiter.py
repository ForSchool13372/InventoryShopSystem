from fastapi import Depends
from app.core.deps import getCurrentGame
from app.core.redisClient import redisClient

def rateLimiter(action: str, limit: int = 5, window: int = 1):
    def dependency(game=Depends(getCurrentGame)):
        key = f"ratelimit:{action}:{game.playerId}"
        count = redisClient.incr(key)

        if count == 1:
            redisClient.expire(key, window)

        if count > limit:
            return False

        return True

    return dependency