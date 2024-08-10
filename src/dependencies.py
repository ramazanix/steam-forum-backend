from aiohttp import ClientSession
from aiocache import SimpleMemoryCache
from src.cache import cache_manager
from src.schemas.auth import Token
from src.security import verify_jwt
from fastapi import Request, HTTPException


async def get_aiohttp_session() -> ClientSession:
    async with ClientSession() as session:
        yield session


def get_cache() -> SimpleMemoryCache:
    yield cache_manager.cache_instance


def protected_route(req: Request) -> Token:
    auth_header = req.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authentication header")

    auth_header = auth_header.split()

    if len(auth_header) != 2 or auth_header[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Not Authorized")
    _, token = auth_header

    if token is None:
        raise HTTPException(status_code=401, detail="Token is missing")

    decoded_token = verify_jwt(token)

    if decoded_token is None:
        raise HTTPException(status_code=401, detail="Token is invalid")

    return decoded_token
