import redis.asyncio as aioredis

from app.domains.account.application.port.user_token_port import UserTokenPort

USER_TOKEN_PREFIX = "user_token:"
KAKAO_TOKEN_PREFIX = "kakao_token:"


class UserTokenRedisAdapter(UserTokenPort):

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def save_user_token(self, user_token: str, account_id: str, ttl_seconds: int) -> None:
        key = f"{USER_TOKEN_PREFIX}{user_token}"
        await self._redis.set(key, account_id, ex=ttl_seconds)

    async def save_kakao_access_token(self, account_id: str, kakao_access_token: str, ttl_seconds: int) -> None:
        key = f"{KAKAO_TOKEN_PREFIX}{account_id}"
        await self._redis.set(key, kakao_access_token, ex=ttl_seconds)

    async def delete_user_token(self, user_token: str) -> None:
        key = f"{USER_TOKEN_PREFIX}{user_token}"
        await self._redis.delete(key)

    async def delete_kakao_access_token(self, account_id: str) -> None:
        key = f"{KAKAO_TOKEN_PREFIX}{account_id}"
        await self._redis.delete(key)
