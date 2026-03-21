import redis.asyncio as aioredis

from app.domains.kakao_authentication.application.port.user_session_port import UserSessionPort

SESSION_KEY_PREFIX = "session:"
KAKAO_TOKEN_PREFIX = "kakao_token:"


class UserSessionRedisAdapter(UserSessionPort):

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def save_user_token(self, user_token: str, account_id: str, ttl_seconds: int) -> None:
        key = f"{SESSION_KEY_PREFIX}{user_token}"
        await self._redis.set(key, account_id, ex=ttl_seconds)

    async def save_kakao_access_token(self, account_id: str, kakao_access_token: str, ttl_seconds: int) -> None:
        key = f"{KAKAO_TOKEN_PREFIX}{account_id}"
        await self._redis.set(key, kakao_access_token, ex=ttl_seconds)
