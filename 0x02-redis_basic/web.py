#!/usr/bin/env python3
'''A module with tools for request caching and tracking.'''
import requests
import redis
from functools import wraps
from typing import Callable


def count_calls(method: Callable) -> Callable:
    '''Decorator to track the number of times a method is called.'''
    @wraps(method)
    def invoker(self, *args, **kwargs):
        '''Increments the method call count.'''
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


class Cache:
    '''Represents an object for caching and tracking URL accesses.'''
    def __init__(self) -> None:
        '''Initializes a Cache instance.'''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def get_page(self, url: str) -> str:
        '''Fetches and caches HTML content from a given URL.'''
        cached_html = self._redis.get(url)
        if cached_html:
            return cached_html.decode('utf-8')

        response = requests.get(url)
        html_content = response.text
        self._redis.setex(url, 10, html_content)
        return html_content
