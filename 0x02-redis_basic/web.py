#!/usr/bin/env python3
"""Module for implementing an expiring web cache and tracker.
"""
import redis
import requests

redis_instance = redis.Redis()
"""Module-level Redis instance for caching.
"""

def cache_expiration(method):
    """Decorator for caching the output of a fetched web page
    with expiration time.
    """
    def wrapper(url):
        """Wrapper function for caching the output.
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

@cache_expiration
def get_page(url):
    """Function to obtain the HTML content of a URL and return it.
    """
    return requests.get(url)
