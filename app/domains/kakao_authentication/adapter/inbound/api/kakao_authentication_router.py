from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse

from app.domains.kakao_authentication.application.response.kakao_user_info_response import KakaoUserInfoResponse
from app.domains.kakao_authentication.application.usecase.request_access_token_usecase import RequestAccessTokenUseCase
from app.domains.kakao_authentication.application.usecase.request_kakao_oauth_link_usecase import (
    RequestKakaoOAuthLinkUseCase,
)
from app.domains.kakao_authentication.di import (
    get_request_access_token_usecase,
    get_request_kakao_oauth_link_usecase,
)

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])


@router.get("/request-oauth-link", status_code=302)
def request_oauth_link(
    usecase: RequestKakaoOAuthLinkUseCase = Depends(get_request_kakao_oauth_link_usecase),
):
    response = usecase.execute()
    return RedirectResponse(url=response.url)


@router.get("/request-access-token-after-redirection", response_model=KakaoUserInfoResponse)
async def request_access_token_after_redirection(
    code: str = Query(..., description="Authorization code from Kakao"),
    usecase: RequestAccessTokenUseCase = Depends(get_request_access_token_usecase),
):
    return await usecase.execute(code=code)
