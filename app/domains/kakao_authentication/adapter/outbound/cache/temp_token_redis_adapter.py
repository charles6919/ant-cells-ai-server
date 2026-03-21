import json

import redis.asyncio as aioredis

from app.domains.kakao_authentication.application.port.temp_token_port import TempTokenPort

TEMP_TOKEN_PREFIX = "temp_token:"


class TempTokenRedisAdapter(TempTokenPort):

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def save(
        self,
        token: str,
        kakao_access_token: str,
        nickname: str,
        email: str,
        ttl_seconds: int,
    ) -> None:
        key = f"{TEMP_TOKEN_PREFIX}{token}"
        payload = json.dumps({
            "kakao_access_token": kakao_access_token,
            "nickname": nickname,
            "email": email,
        })
        await self._redis.set(key, payload, ex=ttl_seconds)
