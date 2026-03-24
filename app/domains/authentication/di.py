from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.account.adapter.outbound.persistence.account_persistence_adapter import AccountPersistenceAdapter
from app.domains.authentication.adapter.outbound.cache.temp_token_lookup_redis_adapter import TempTokenLookupRedisAdapter
from app.domains.authentication.adapter.outbound.cache.user_session_lookup_redis_adapter import UserSessionLookupRedisAdapter
from app.domains.authentication.application.usecase.get_user_info_usecase import GetUserInfoUseCase
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.database.database import get_db_session


def get_user_info_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetUserInfoUseCase:
    redis = get_redis_client()
    return GetUserInfoUseCase(
        temp_token_lookup=TempTokenLookupRedisAdapter(redis_client=redis),
        user_session_lookup=UserSessionLookupRedisAdapter(redis_client=redis),
        account_repository=AccountPersistenceAdapter(session=session),
    )
