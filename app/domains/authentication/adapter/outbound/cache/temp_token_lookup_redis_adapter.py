import json
from typing import Optional

import redis.asyncio as aioredis

from app.domains.authentication.application.port.temp_token_lookup_port import TempTokenLookupPort
from app.domains.authentication.domain.entity.temp_user_info import TempUserInfo

TEMP_TOKEN_PREFIX = "temp_token:"


class TempTokenLookupRedisAdapter(TempTokenLookupPort):

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def get_user_info(self, token: str) -> Optional[TempUserInfo]:
        key = f"{TEMP_TOKEN_PREFIX}{token}"
        raw = await self._redis.get(key)
        if raw is None:
            return None
        data = json.loads(raw)
        return TempUserInfo(
            nickname=data.get("nickname"),
            email=data.get("email"),
        )
