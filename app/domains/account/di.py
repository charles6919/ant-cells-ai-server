from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.account.adapter.outbound.cache.temp_token_validation_redis_adapter import TempTokenValidationRedisAdapter
from app.domains.account.adapter.outbound.cache.user_token_redis_adapter import UserTokenRedisAdapter
from app.domains.account.adapter.outbound.persistence.account_persistence_adapter import AccountPersistenceAdapter
from app.domains.account.application.usecase.register_account_usecase import RegisterAccountUseCase
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.database.database import get_db_session


def get_account_persistence_adapter(
    session: AsyncSession = Depends(get_db_session),
) -> AccountPersistenceAdapter:
    return AccountPersistenceAdapter(session=session)


def get_register_account_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> RegisterAccountUseCase:
    redis = get_redis_client()
    return RegisterAccountUseCase(
        account_repository=AccountPersistenceAdapter(session=session),
        temp_token=TempTokenValidationRedisAdapter(redis_client=redis),
        user_token=UserTokenRedisAdapter(redis_client=redis),
    )
