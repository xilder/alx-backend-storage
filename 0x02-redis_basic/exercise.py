#!/usr/bin/env python3
"""creates a Cache class using the redis module"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    counts how many times the
    methods of a class are called
    """
    @wraps(method)
    def count(self, *args, **kwargs):
        """counter for the function called"""
        if (isinstance(self._redis, redis.Redis)):
            self._redis.incr(method.__qualname.__)
        return method(self, *args, **kwargs)
    return count


class Cache:
    """Cache class using redis"""
    def __init__(self):
        """creates an instance of redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores a data value using a random key
        in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Callable = None
    ) -> Union[str, int, bytes, float]:
        """
        Gets a value by its key from Redis db
        Converts the value if callable fn is not none
        """
        value = self._redis.get(key)
        if fn is not None and value is not None:
            value = fn(value)
        return value
