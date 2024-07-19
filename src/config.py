from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    STEAM_API_KEY: str
    BACKEND_URL: str
    FRONTEND_URL: str
    FRONTEND_AUTH_CALLBACK_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
