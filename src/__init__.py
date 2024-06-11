from fastapi import FastAPI
from src.config import settings


def init_app():
    server = FastAPI(title="Steam Forum")

    from src.routers.auth import auth_router

    server.include_router(auth_router)

    return server
