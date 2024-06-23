#!/usr/bin/env python3
"""creates a Cache class using the redis module"""

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    counts how many times the
    methods of a class are called
    """
    @wraps(method)
    def count(self, *args, **kwargs) -> Any:
        """counter for the function called"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return count


def call_history(method: Callable) -> Callable:
    """
    stores the history of every method call
    """
    @wraps(method)
    def history(self, *args, **kwargs) -> Any:
        """stores the history of a method (its inputs and output)"""
        if isinstance(self._redis, redis.Redis):
            results = method(self, *args, **kwargs)
            self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
            self._redis.rpush(f"{method.__qualname__}:outputs", str(results))
            return results
    return history


def replay(method: Callable) -> Any:
    """
    replays the history of a function including inputs and output
    """
    if method is None or not hasattr(method, "__self__"):
        return
    redis_db = getattr(method.__self__, "_redis")
    inputs = redis_db.lrange(f"{method.__qualname__}:inputs", 0, -1)
    outputs = redis_db.lrange(f"{method.__qualname__}:outputs", 0, -1)
    print(f"{method.__qualname__} was called {len(outputs)} times:")
    for i, o in zip(inputs, outputs):
        i = i.decode('utf-8')
        o = o.decode('utf-8')
        print(f"{method.__qualname__}(*{i}) -> {o}")


class Cache:
    """Cache class using redis"""
    def __init__(self):
        """creates an instance of redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores a data value using a random key
        in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @call_history
    @count_calls
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
