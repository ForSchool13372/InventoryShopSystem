import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

redisUrl = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

celeryApp = Celery(
    "inventoryShop",
    broker=redisUrl,
    backend=redisUrl,
)