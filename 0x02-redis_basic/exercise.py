#!/usr/bin/env python3
"""
Redis Basic exercises
"""
import redis
import uuid
from typing import Callable


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str):
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str):
        return self.get(key, fn=int)

    def count_calls(func):
        def wrapper(self, *args, **kwargs):
            key = func.__qualname__
            self._redis.incr(key)
            return func(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def call_history(func):
        def wrapper(self, *args, **kwargs):
            key = f"{func.__qualname__}:inputs"
            self._redis.rpush(key, str(args))
            output = func(self, *args, **kwargs)
            key = f"{func.__qualname__}:outputs"
            self._redis.rpush(key, str(output))
            return output
        return wrapper

    @call_history
    def store(self, data) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(self, fn):
        inputs = self._redis.lrange(f"{fn.__qualname__}:inputs", 0, -1)
        outputs = self._redis.lrange(f"{fn.__qualname__}:outputs", 0, -1)
        print(f"{fn.__qualname__} was called {len(inputs)} times:")
        for input_val, output_val in zip(inputs, outputs):
            print(f"{fn}{input_val} -> {output_val}")


if __name__ == '__main__':
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

    cache = Cache()
    cache.store(b"first")
    print(cache._redis.get(cache.store.__qualname__))  # Output: b'1'
