from typing import Optional

import redis.asyncio as aioredis

from app.domains.account.application.port.user_token_read_port import UserTokenReadPort

SESSION_KEY_PREFIX = "session:"


class UserTokenReadRedisAdapter(UserTokenReadPort):
    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def get_account_id(self, user_token: str) -> Optional[str]:
        key = f"{SESSION_KEY_PREFIX}{user_token}"
        return await self._redis.get(key)
