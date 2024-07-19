from aiocache import SimpleMemoryCache


class CacheManager:
    def __init__(self):
        self.cache_instance = None

    def get_cache(self):
        if self.cache_instance is None:
            self.cache_instance = SimpleMemoryCache()
        return self.cache_instance


cache_manager = CacheManager()
