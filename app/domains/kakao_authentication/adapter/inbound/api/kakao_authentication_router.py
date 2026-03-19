from fastapi import APIRouter, Depends, Query, Response
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

TEMP_TOKEN_COOKIE_KEY = "temp_token"
TEMP_TOKEN_TTL_SECONDS = 300  # 5 minutes


@router.get("/request-oauth-link", status_code=302)
def request_oauth_link(
    usecase: RequestKakaoOAuthLinkUseCase = Depends(get_request_kakao_oauth_link_usecase),
):
    response = usecase.execute()
    return RedirectResponse(url=response.url)


@router.get(
    "/request-access-token-after-redirection",
    response_model=KakaoUserInfoResponse,
    response_model_exclude={"temp_token"},
)
async def request_access_token_after_redirection(
    response: Response,
    code: str = Query(..., description="Authorization code from Kakao"),
    usecase: RequestAccessTokenUseCase = Depends(get_request_access_token_usecase),
):
    result = await usecase.execute(code=code)

    if result.temp_token:
        response.set_cookie(
            key=TEMP_TOKEN_COOKIE_KEY,
            value=result.temp_token,
            httponly=True,
            max_age=TEMP_TOKEN_TTL_SECONDS,
            samesite="lax",
        )

    return result
