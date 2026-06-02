import os
import redis

redisClient = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 19222)),
    username=os.getenv("REDIS_USER"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)