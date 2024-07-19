from aiohttp import ClientSession
from aiocache import SimpleMemoryCache
from src.cache import cache_manager


async def get_aiohttp_session() -> ClientSession:
    async with ClientSession() as session:
        yield session


async def get_cache() -> SimpleMemoryCache:
    yield cache_manager.get_cache()
