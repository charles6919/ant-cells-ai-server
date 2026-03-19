from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.account.adapter.outbound.persistence.account_persistence_adapter import AccountPersistenceAdapter
from app.domains.kakao_authentication.adapter.outbound.cache.temp_token_redis_adapter import TempTokenRedisAdapter
from app.domains.kakao_authentication.adapter.outbound.external.kakao_oauth_adapter import KakaoOAuthAdapter
from app.domains.kakao_authentication.adapter.outbound.external.kakao_token_adapter import KakaoTokenAdapter
from app.domains.kakao_authentication.adapter.outbound.external.kakao_user_info_adapter import KakaoUserInfoAdapter
from app.domains.kakao_authentication.application.usecase.request_access_token_usecase import RequestAccessTokenUseCase
from app.domains.kakao_authentication.application.usecase.request_kakao_oauth_link_usecase import (
    RequestKakaoOAuthLinkUseCase,
)
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.database.database import get_db_session


def get_request_kakao_oauth_link_usecase() -> RequestKakaoOAuthLinkUseCase:
    return RequestKakaoOAuthLinkUseCase(kakao_oauth=KakaoOAuthAdapter())


def get_request_access_token_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> RequestAccessTokenUseCase:
    return RequestAccessTokenUseCase(
        kakao_token=KakaoTokenAdapter(),
        kakao_user_info=KakaoUserInfoAdapter(),
        account_repository=AccountPersistenceAdapter(session=session),
        temp_token=TempTokenRedisAdapter(redis_client=get_redis_client()),
    )
