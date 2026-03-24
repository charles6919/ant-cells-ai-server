from typing import Optional

import redis.asyncio as aioredis

from app.domains.authentication.application.port.user_session_lookup_port import UserSessionLookupPort

SESSION_KEY_PREFIX = "session:"


class UserSessionLookupRedisAdapter(UserSessionLookupPort):

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def get_account_id(self, user_token: str) -> Optional[str]:
        key = f"{SESSION_KEY_PREFIX}{user_token}"
        return await self._redis.get(key)
