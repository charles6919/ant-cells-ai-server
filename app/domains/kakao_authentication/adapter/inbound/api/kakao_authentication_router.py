from urllib.parse import quote

from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse

from app.domains.kakao_authentication.application.usecase.request_access_token_usecase import RequestAccessTokenUseCase
from app.domains.kakao_authentication.application.usecase.request_kakao_oauth_link_usecase import (
    RequestKakaoOAuthLinkUseCase,
)
from app.domains.kakao_authentication.di import (
    get_request_access_token_usecase,
    get_request_kakao_oauth_link_usecase,
)
from app.infrastructure.config import get_settings

router = APIRouter(prefix="/kakao-authentication", tags=["kakao-authentication"])

TEMP_TOKEN_COOKIE_KEY = "temp_token"
TEMP_TOKEN_TTL_SECONDS = 300   # 5 minutes
USER_TOKEN_COOKIE_KEY = "user_token"
SESSION_TTL_SECONDS = 3600     # 1 hour


@router.get("/request-oauth-link", status_code=302)
def request_oauth_link(
    usecase: RequestKakaoOAuthLinkUseCase = Depends(get_request_kakao_oauth_link_usecase),
):
    response = usecase.execute()
    return RedirectResponse(url=response.url)


@router.get("/request-access-token-after-redirection")
async def request_access_token_after_redirection(
    code: str = Query(..., description="Authorization code from Kakao"),
    usecase: RequestAccessTokenUseCase = Depends(get_request_access_token_usecase),
):
    settings = get_settings()
    result = await usecase.execute(code=code)

    redirect_response = RedirectResponse(url=f"{settings.CORS_ALLOWED_FRONTEND_URL}/auth-callback")

    if result.user_token:
        redirect_response.set_cookie(
            key=USER_TOKEN_COOKIE_KEY,
            value=result.user_token,
            httponly=True,
            max_age=SESSION_TTL_SECONDS,
            samesite="lax",
        )
        redirect_response.set_cookie(
            key="nickname",
            value=quote(result.nickname or "", safe=""),
            httponly=True,
            max_age=SESSION_TTL_SECONDS,
            samesite="lax",
        )
        redirect_response.set_cookie(
            key="email",
            value=quote(result.email or "", safe=""),
            httponly=True,
            max_age=SESSION_TTL_SECONDS,
            samesite="lax",
        )

    if result.temp_token:
        redirect_response.set_cookie(
            key=TEMP_TOKEN_COOKIE_KEY,
            value=result.temp_token,
            httponly=True,
            max_age=TEMP_TOKEN_TTL_SECONDS,
            samesite="lax",
        )

    return redirect_response
