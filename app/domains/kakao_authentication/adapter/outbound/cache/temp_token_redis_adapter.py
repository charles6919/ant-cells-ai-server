import redis.asyncio as aioredis

from app.domains.kakao_authentication.application.port.temp_token_port import TempTokenPort

TEMP_TOKEN_PREFIX = "temp_token:"


class TempTokenRedisAdapter(TempTokenPort):

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def save(self, token: str, kakao_access_token: str, ttl_seconds: int) -> None:
        key = f"{TEMP_TOKEN_PREFIX}{token}"
        await self._redis.set(key, kakao_access_token, ex=ttl_seconds)
