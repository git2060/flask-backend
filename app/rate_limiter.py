import os
import time
from flask import request, jsonify
from app.redis_client import redis_client

RATE_LIMIT = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))

def rate_limit():
    """
    Simple Redis-backed rate limiting.
    Limits requests per IP per time window.
    """
    if not redis_client:
        # Fail open if Redis is down
        return None

    ip = request.remote_addr or "unknown"
    key = f"rate:{ip}:{int(time.time() // WINDOW)}"

    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, WINDOW)

    if current > RATE_LIMIT:
        return jsonify({
            "error": "Too many requests",
            "detail": f"Rate limit exceeded ({RATE_LIMIT}/{WINDOW}s)"
        }), 429

    return None
