from pydantic import BaseModel, HttpUrl
from datetime import datetime


class SteamUserInfo(BaseModel):
    steamid: str
    communityvisibilitystate: int
    profilestate: int
    personaname: str
    commentpermission: int
    profileurl: HttpUrl
    avatar: HttpUrl
    avatarmedium: HttpUrl
    avatarfull: HttpUrl
    avatarhash: str
    lastlogoff: int
    personastate: int
    primaryclanid: str
    timecreated: int
    personastateflags: int
    loccountrycode: str
    locstatecode: str
    loccityid: int


class Token(BaseModel):
    exp: datetime
    sub: SteamUserInfo
