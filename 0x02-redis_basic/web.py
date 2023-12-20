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

def cache_tracker(method: Callable) -> Callable:
    """A decorator to cache fetched web data with tracking.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function to cache the output.
        """
        redis_instance.incr(f'count:{url}')
        result = redis_instance.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        response = method(url)
        redis_instance.set(f'count:{url}', 0)
        redis_instance.setex(f'result:{url}', 10, response.text)
        return response.text
    return wrapper

@cache_tracker
def get_page(url: str) -> str:
    """Function to fetch HTML content from a URL and return it.
    """
    return requests.get(url).text
