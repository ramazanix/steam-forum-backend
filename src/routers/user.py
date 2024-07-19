import datetime
from typing import Annotated
from aiocache import BaseCache
from aiohttp import ClientSession
from fastapi import APIRouter, Depends
from src.dependencies import get_aiohttp_session, get_cache
from src.schemas.user import UserInventoryResponse
from src.utils import parse_user_inventory
from src.enums import SteamAppIds, SteamCurrencies

users_router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@users_router.get("/{user_id}/inventory/", response_model=UserInventoryResponse)
async def get_user_inventory(
    user_id: str,
    game: SteamAppIds,
    currency: SteamCurrencies,
    aiohttp_session: Annotated[ClientSession, Depends(get_aiohttp_session)],
    cache: Annotated[BaseCache, Depends(get_cache)],
):
    if await cache.exists(user_id, "inventory"):
        return await cache.get(user_id, namespace="inventory")

    res = await parse_user_inventory(user_id, game, currency, aiohttp_session)
    await cache.set(user_id, res, ttl=300, namespace="inventory")

    return res
