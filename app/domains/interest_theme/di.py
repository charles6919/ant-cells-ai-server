from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.interest_theme.adapter.outbound.cache.user_token_read_redis_adapter import UserTokenReadRedisAdapter
from app.domains.interest_theme.adapter.outbound.persistence.theme_persistence_adapter import ThemePersistenceAdapter
from app.domains.interest_theme.adapter.outbound.persistence.user_interest_theme_persistence_adapter import UserInterestThemePersistenceAdapter
from app.domains.interest_theme.application.usecase.get_all_themes_usecase import GetAllThemesUseCase
from app.domains.interest_theme.application.usecase.get_my_interest_themes_usecase import GetMyInterestThemesUseCase
from app.domains.interest_theme.application.usecase.save_user_interest_themes_usecase import SaveUserInterestThemesUseCase
from app.domains.interest_theme.application.usecase.update_interest_themes_usecase import UpdateInterestThemesUseCase
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.database.database import get_db_session


def get_all_themes_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetAllThemesUseCase:
    return GetAllThemesUseCase(
        theme_repository=ThemePersistenceAdapter(session=session),
    )


def get_save_user_interest_themes_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> SaveUserInterestThemesUseCase:
    return SaveUserInterestThemesUseCase(
        user_interest_theme_repository=UserInterestThemePersistenceAdapter(session=session),
    )


def get_my_interest_themes_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetMyInterestThemesUseCase:
    redis = get_redis_client()
    return GetMyInterestThemesUseCase(
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
        user_interest_theme_repository=UserInterestThemePersistenceAdapter(session=session),
    )


def get_update_interest_themes_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> UpdateInterestThemesUseCase:
    redis = get_redis_client()
    return UpdateInterestThemesUseCase(
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
        theme_repository=ThemePersistenceAdapter(session=session),
        user_interest_theme_repository=UserInterestThemePersistenceAdapter(session=session),
    )
