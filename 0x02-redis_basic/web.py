#!/usr/bin/env python3
"""A module for request caching and tracking tools.
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_instance = redis.Redis()
"""The module-level Redis instance.
"""

def data_cacher(method: Callable) -> Callable:
    """Caches the output of fetched data.
    """
    @wraps(method)
    def invoker(url: str) -> str:
        """Wrapper function for caching the output.
        """
        redis_instance.incr(f'count:{url}')
        result = redis_instance.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        response = method(url)
        redis_instance.set(f'result:{url}', response.text, ex=10)
        return response.text
    return invoker

@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response
    and tracking the request.
    """
    return requests.get(url)
