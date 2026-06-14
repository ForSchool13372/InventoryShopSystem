import os
from dotenv import load_dotenv
import redis

# load environment variables
load_dotenv()

# Redis client
redisClient = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    username=os.getenv("REDIS_USER"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)

# optional: quick health check (safe for production startup)
def checkRedisConnection():
    try:
        return redisClient.ping()
    except Exception:
        return False