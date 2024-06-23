#!/usr/bin/env python3
"""creates a Cache class using the redis module"""

import redis
import uuid
from typing import Union


class Cache:
    """Cache class using redis"""
    def __init__(self):
        """creates an instance of redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores a data value using a random key
        in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
