import os
from dotenv import load_dotenv
import redis

load_dotenv()

# =========================================================
# REDIS CLIENT (LAZY INIT - SAFE FOR TESTS + CI)
# =========================================================

redisClient = None


def initRedis():
    global redisClient

    redisClient = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        username=os.getenv("REDIS_USER"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
    )


# =========================================================
# OPTIONAL HEALTH CHECK
# =========================================================

def checkRedisConnection():
    try:
        if redisClient is None:
            return False
        return redisClient.ping()
    except Exception:
        return False