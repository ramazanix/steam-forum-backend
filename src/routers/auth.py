from typing import Annotated
from aiohttp import ClientSession
from src.dependencies import get_aiohttp_session
from src.security import create_access_token
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from src.utils import get_user_info
from src.config import settings
from urllib import parse

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# Конфигурация Steam OpenID Connect
STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"
STEAM_API_KEY = settings.STEAM_API_KEY
REDIRECT_URI = f"{settings.BACKEND_URL}/auth/callback"


@auth_router.get("/login")
async def login():
    """
    Обработчик для перенаправления пользователя на страницу аутентификации Steam.
    """
    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": REDIRECT_URI,
        "openid.realm": REDIRECT_URI,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
    }
    return RedirectResponse(url=f"{STEAM_OPENID_URL}?{parse.urlencode(params)}")


@auth_router.get("/callback")
async def auth_callback(
    request: Request,
    aiohttp_session: Annotated[ClientSession, Depends(get_aiohttp_session)],
):
    """
    Обработчик для обработки ответа от Steam после аутентификации.
    """
    params = request.query_params

    if "openid.mode" not in params or params["openid.mode"] != "id_res":
        raise HTTPException(
            status_code=400,
            detail="Invalid OpenID response",
        )

    # Проверка подлинности ответа от Steam
    async with aiohttp_session.get(
        STEAM_OPENID_URL,
        params={
            "openid.assoc_handle": params["openid.assoc_handle"],
            "openid.signed": params["openid.signed"],
            "openid.sig": params["openid.sig"],
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.mode": "check_authentication",
            "openid.op_endpoint": params["openid.op_endpoint"],
            "openid.claimed_id": params["openid.claimed_id"],
            "openid.identity": params["openid.identity"],
            "openid.return_to": params["openid.return_to"],
            "openid.response_nonce": params["openid.response_nonce"],
        },
    ) as response:

        if "is_valid:true" not in response.text:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenID response",
            )

        # Извлечение информации о пользователе
        user_id = params["openid.claimed_id"].split("/")[-1]
        user_info = await get_user_info(user_id, aiohttp_session)

    # Генерация JWT токена
    access_token = create_access_token(user_info)

    # Возврат JWT токена в качестве ответа
    response = RedirectResponse(
        url=f"{settings.FRONTEND_AUTH_CALLBACK_URL}/?accessToken={access_token}"
    )
    return response
