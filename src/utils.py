import asyncio
from aiohttp import ClientSession
from src.config import settings
from src.schemas.user import (
    UserInventoryFromSteam,
    UserInventoryResponse,
    InventoryItemPriceInfo,
    UserInventoryItem,
)
from src.enums import SteamCurrencies, SteamAppIds


async def get_user_info(
    user_id,
    aiohttp_session: ClientSession,
):
    async with aiohttp_session.get(
        f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/"
        f"v0002/?key={settings.STEAM_API_KEY}&steamids={user_id}"
    ) as resp:
        response = await resp.json()

    return response["response"]["players"][0]


async def get_item_price(
    app: SteamAppIds,
    market_hash_name: str,
    currency: SteamCurrencies,
    session: ClientSession,
):
    async with session.get(
        f"https://steamcommunity.com/market/priceoverview/"
        f"?appid={app.value}&currency={currency.value}"
        f"&market_hash_name={market_hash_name}"
    ) as resp:
        if resp.status != 200:
            return None

        item_price_response = await resp.json()

    return InventoryItemPriceInfo(**item_price_response)


async def parse_user_inventory(
    user_id: str,
    app: SteamAppIds,
    currency: SteamCurrencies,
    aiohttp_session: ClientSession,
) -> UserInventoryResponse:
    async with aiohttp_session.get(
        f"https://steamcommunity.com/inventory/{user_id}/{app.value}/2?l=russian&count=1000"
    ) as resp:
        raw_inventory_data = await resp.json()

    user_inv = UserInventoryFromSteam(**raw_inventory_data)
    response_data = UserInventoryResponse(appid=app.value)

    tradable_items = filter(
        lambda x: x.marketable,
        user_inv.descriptions,
    )

    async def fetch_price(item: UserInventoryItem):
        it = UserInventoryItem(**item.__dict__)
        it.price_info = await get_item_price(
            app, item.market_hash_name, currency, aiohttp_session
        )
        return it

    tasks = [fetch_price(item) for item in tradable_items]
    response_data.items = await asyncio.gather(*tasks)

    return response_data
