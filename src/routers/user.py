import datetime
from typing import Annotated
from aiocache import BaseCache
from aiohttp import ClientSession
from fastapi import APIRouter, Depends
from src.dependencies import get_aiohttp_session, get_cache, protected_route
from src.schemas.user import UserInventoryResponse
from src.schemas.auth import SteamUserInfo
from src.utils import parse_user_inventory
from src.enums import SteamAppIds, SteamCurrencies

users_router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@users_router.get("/inventory", response_model=UserInventoryResponse)
async def get_user_inventory(
    game: SteamAppIds,
    currency: SteamCurrencies,
    aiohttp_session: Annotated[ClientSession, Depends(get_aiohttp_session)],
    cache: Annotated[BaseCache, Depends(get_cache)],
    current_user: Annotated[SteamUserInfo, Depends(protected_route)],
):
    user_id = current_user.steamid

    if await cache.exists(user_id, "inventory"):
        print("inventory was in cache")
        return await cache.get(user_id, namespace="inventory")

    res = await parse_user_inventory(user_id, game, currency, aiohttp_session)
    await cache.set(user_id, res.model_dump(), ttl=300, namespace="inventory")
    print("inventory cached")
    return res
