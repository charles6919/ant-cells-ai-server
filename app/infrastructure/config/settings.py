from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str
    JWT_SECRET_KEY: str
    SERP_API_KEY: str
    OPENAI_API_KEY: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    SESSION_TTL_SECONDS: int = 3600
    AUTH_PASSWORD: str
    KAKAO_CLIENT_ID: str
    KAKAO_REDIRECT_URI: str
    CORS_ALLOWED_FRONTEND_URL: str = "http://localhost:3000"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
