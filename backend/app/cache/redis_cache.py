"""Memory Cache: 内存缓存，兜底方案"""
import time


class MemoryCache:
    def __init__(self, max_size: int = 100):
        self._store = {}
        self._max_size = max_size

    def get(self, key: str):
        entry = self._store.get(key)
        if entry and entry["expire"] > time.time():
            return entry["value"]
        if entry:
            del self._store[key]
        return None

    def set(self, key: str, value: str, ttl: int = 600):
        if len(self._store) >= self._max_size:
            oldest = min(self._store, key=lambda k: self._store[k]["expire"])
            del self._store[oldest]
        self._store[key] = {"value": value, "expire": time.time() + ttl}


_memory_cache = MemoryCache()


def get_cache():
    return _memory_cache
