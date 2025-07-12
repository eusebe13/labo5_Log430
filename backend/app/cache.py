import json
import os

import redis

# Connexion Redis (valeurs par défaut pour docker-compose)
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0)

def set_cache(key: str, data, ttl: int = 60):
    r.setex(key, ttl, json.dumps(data))

def get_cache(key: str):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    return None

def delete_cache(key: str):
    r.delete(key)
