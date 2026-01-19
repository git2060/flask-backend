import os
import redis
import logging

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def get_redis():
    try:
        client = redis.Redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=1
        )
        client.ping()
        return client
    except redis.RedisError as e:
        logger.warning(f"Redis unavailable: {e}")
        return None

redis_client = get_redis()
