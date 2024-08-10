from datetime import (
    datetime,
    timezone,
    timedelta,
)
from fastapi import HTTPException
from src.config import settings
from jwt.exceptions import InvalidSignatureError
from jwt import encode as jwt_encode, decode as jwt_decode

from src.schemas.auth import Token


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.ACCESS_EXPIRES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def verify_jwt(token: str) -> Token | None:
    try:
        # decoded_token = Token(
        #     **jwt_decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # )
        decoded_token = Token(**{'sub' :{'steamid': '76561198123348624', 'communityvisibilitystate': 3, 'profilestate': 1,
                          'personaname': 'Uebki Suka', 'commentpermission': 1,
                          'profileurl': 'https://steamcommunity.com/id/ramazanix/',
                          'avatar': 'https://avatars.steamstatic.com/0b077d90207471add379fa37f276d13c71bd5979.jpg',
                          'avatarmedium': 'https://avatars.steamstatic.com/0b077d90207471add379fa37f276d13c71bd5979_medium.jpg',
                          'avatarfull': 'https://avatars.steamstatic.com/0b077d90207471add379fa37f276d13c71bd5979_full.jpg',
                          'avatarhash': '0b077d90207471add379fa37f276d13c71bd5979', 'lastlogoff': 1721534889,
                          'personastate': 0, 'primaryclanid': '103582791429670253', 'timecreated': 1390052137,
                          'personastateflags': 0, 'loccountrycode': 'FI', 'locstatecode': '06', 'loccityid': 15506}, 'exp': 1821556160})
        return (
            decoded_token.sub
            if decoded_token.exp > datetime.now(timezone.utc)
            else None
        )

    except InvalidSignatureError:
        return None
