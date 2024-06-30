from pydantic import BaseModel


class InventoryItemFromSteam(BaseModel):
    appid: int
    contextid: str
    assetid: str
    classid: str
    instanceid: str
    amount: str


class ItemDescriptionFromSteam(BaseModel):
    type: str = ""
    value: str
    color: str = ""


class ItemTagFromSteam(BaseModel):
    category: str
    internal_name: str
    localized_category_name: str
    localized_tag_name: str
    color: str = ""


class InventoryDescriptionFromSteam(BaseModel):
    appid: int
    classid: str
    instanceid: str
    currency: int
    background_color: str
    icon_url: str
    icon_url_large: str = ""
    descriptions: list[ItemDescriptionFromSteam] = []
    tradable: int
    name: str
    name_color: str
    type: str
    market_name: str
    market_hash_name: str
    commodity: int
    market_tradable_restriction: int
    market_marketable_restriction: int
    marketable: int
    tags: list[ItemTagFromSteam]
    item_expiration: str = ""


class UserInventoryFromSteam(BaseModel):
    assets: list[InventoryItemFromSteam]
    descriptions: list[InventoryDescriptionFromSteam]
    total_inventory_count: int
    success: int


class InventoryItemPriceInfo(BaseModel):
    lowest_price: str
    median_price: str = ""


class UserInventoryItem(BaseModel):
    instanceid: str
    currency: int
    background_color: str
    icon_url: str
    icon_url_large: str = ""
    descriptions: list[ItemDescriptionFromSteam]
    tradable: int
    name: str
    name_color: str
    type: str
    market_name: str
    market_hash_name: str
    tags: list[ItemTagFromSteam]
    price_info: InventoryItemPriceInfo | None = None


class UserInventoryResponse(BaseModel):
    appid: int
    items: list[UserInventoryItem] = []
