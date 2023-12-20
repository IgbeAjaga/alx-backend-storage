#!/usr/bin/env python3
"""A module for request caching and tracking tools.
"""
import redis
import requests

redis_instance = redis.Redis()
"""The module-level Redis instance.
"""


def get_page(url: str) -> str:
    """Retrieves HTML content from a URL and caches the response for 10 seconds.
    Tracks the number of times the URL was accessed.
    """
    redis_instance.incr(f'count:{url}')
    cached_response = redis_instance.get(f'result:{url}')

    if cached_response:
        return cached_response.decode('utf-8')

    response = requests.get(url)
    redis_instance.setex(f'result:{url}', 10, response.text)
    return response.text
