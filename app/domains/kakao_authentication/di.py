from app.domains.kakao_authentication.adapter.outbound.external.kakao_oauth_adapter import KakaoOAuthAdapter
from app.domains.kakao_authentication.adapter.outbound.external.kakao_token_adapter import KakaoTokenAdapter
from app.domains.kakao_authentication.adapter.outbound.external.kakao_user_info_adapter import KakaoUserInfoAdapter
from app.domains.kakao_authentication.application.usecase.request_access_token_usecase import RequestAccessTokenUseCase
from app.domains.kakao_authentication.application.usecase.request_kakao_oauth_link_usecase import (
    RequestKakaoOAuthLinkUseCase,
)


def get_request_kakao_oauth_link_usecase() -> RequestKakaoOAuthLinkUseCase:
    return RequestKakaoOAuthLinkUseCase(kakao_oauth=KakaoOAuthAdapter())


def get_request_access_token_usecase() -> RequestAccessTokenUseCase:
    return RequestAccessTokenUseCase(
        kakao_token=KakaoTokenAdapter(),
        kakao_user_info=KakaoUserInfoAdapter(),
    )
