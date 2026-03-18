import json
from datetime import datetime
from typing import Optional

import redis.asyncio as aioredis

from app.domains.session.application.port.session_store_port import SessionStorePort
from app.domains.session.domain.entity.session_data import SessionData

SESSION_KEY_PREFIX = "session:"


class RedisSessionAdapter(SessionStorePort):
    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def save(self, session: SessionData, ttl_seconds: int) -> None:
        key = SESSION_KEY_PREFIX + session.token
        payload = json.dumps({
            "token": session.token,
            "user_id": session.user_id,
            "role": session.role,
            "created_at": session.created_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
        })
        await self._redis.set(key, payload, ex=ttl_seconds)

    async def find_by_token(self, token: str) -> Optional[SessionData]:
        key = SESSION_KEY_PREFIX + token
        raw = await self._redis.get(key)
        if raw is None:
            return None
        data = json.loads(raw)
        return SessionData(
            token=data["token"],
            user_id=data["user_id"],
            role=data["role"],
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]),
        )

    async def delete(self, token: str) -> None:
        key = SESSION_KEY_PREFIX + token
        await self._redis.delete(key)
