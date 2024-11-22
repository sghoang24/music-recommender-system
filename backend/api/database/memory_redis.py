# pylint: disable=E0401
"""Memory Redis."""

import redis
from core.constant import REDIS_HOST, REDIS_PORT
from redis.client import Redis


class RedisDatabase:
    """Redis database."""

    def __init__(self):
        self.redis_client: Redis = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")

    def push(self, key: str, value: str):
        """Push."""
        self.redis_client.set(key, value)

    def lpush(self, key: str, value: list[str]):
        """Left Push."""
        if isinstance(value, str):
            value = [value]
        self.redis_client.lpush(key, *value)

    def get(self, key: str, value: str):
        """Get."""
        return self.redis_client.get(key).decode("utf-8") == value

    def delete(self, key: str):
        """Delete."""
        self.redis_client.delete(key)

    def get_by_key(self, key: str):
        """Get by key."""
        return self.redis_client.get(key)

    def set_with_expire(self, key: str, value: str, expire: int = 3600):
        """Set with expire."""
        self.redis_client.set(key, value)
        self.redis_client.expire(key, expire)

    def lpush_with_expire(self, key: str, value: list[str] | str, expire: int = 3600):
        """Left Push with expire."""
        if isinstance(value, str):
            value = [value]
        self.redis_client.lpush(key, *value)
        self.redis_client.expire(key, expire)

    def rpop(self, key: str):
        """Right Pop."""
        return self.redis_client.rpop(key)

    # Function for set data structure
    def sadd(self, key: str, value, expire: int = 3600):
        """Set Add."""
        self.redis_client.sadd(key, value)
        self.redis_client.expire(key, expire)

    def spop(self, key: str):
        """Set Pop."""
        return self.redis_client.spop(key)

    def sismember(self, key: str, value):
        """Set IsMember."""
        return self.redis_client.sismember(key, value)

    # Function for counting
    def increase(self, key: str):
        """Increase."""
        self.redis_client.incr(key)

    def decrease(self, key: str):
        """Decrease."""
        self.redis_client.decr(key)


redis_database = RedisDatabase()
