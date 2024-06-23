#!/usr/bin/env python3
"""requests an html page and returns the number of times it was called"""
import requests
import redis
from functools import wraps
from typing import Callable, Any

rd = redis.Redis()


def data_cacher(method: Callable) -> Any:
    """caches the number of times a function a site called"""

    @wraps(method)
    def cacher(url: str) -> str:
        """cache wrapper"""
        rd.incr(f"count:{url}")
        result = rd.get(f"result:{url}")
        if result:
            return result.decode('utf-8')
        result = method(url)
        rd.setex(f"result:{url}", 10, result)
        return result

    return cacher


@data_cacher
def get_page(url: str) -> str:
    """get_page function"""
    res = requests.get(url).text
    return res

