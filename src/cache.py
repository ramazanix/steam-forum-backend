from aiocache import Cache


class CacheManager:
    def __init__(self):
        self._cache_instance = None

    @property
    def cache_instance(self):
        if self._cache_instance is None:
            self._cache_instance = Cache(Cache.REDIS)
        return self._cache_instance


cache_manager = CacheManager()
