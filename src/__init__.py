from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_app():
    server = FastAPI(title="Steam Forum")

    from src.routers.auth import auth_router
    from src.routers.user import users_router

    origins = [
        "https://ramazanix.tech",
        "https://www.ramazanix.tech",
    ]

    server.include_router(auth_router)
    server.include_router(users_router)

    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return server
