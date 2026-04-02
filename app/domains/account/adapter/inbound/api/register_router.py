from urllib.parse import quote

from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import RedirectResponse

from app.domains.account.application.request.register_account_request import RegisterAccountRequest
from app.domains.account.application.usecase.delete_account_usecase import DeleteAccountUseCase
from app.domains.account.application.usecase.register_account_usecase import RegisterAccountUseCase
from app.domains.account.di import get_delete_account_usecase, get_register_account_usecase
from app.infrastructure.config import get_settings

router = APIRouter(prefix="/account", tags=["account"])

USER_TOKEN_COOKIE_KEY = "user_token"
USER_TOKEN_TTL_SECONDS = 3600  # 1 hour


@router.post("/sign-up")
async def register_account(
    request: RegisterAccountRequest,
    temp_token: str = Cookie(..., alias="temp_token"),
    usecase: RegisterAccountUseCase = Depends(get_register_account_usecase),
):
    settings = get_settings()
    account, user_token_value = await usecase.execute(
        temp_token=temp_token,
        nickname=request.nickname,
        email=request.email,
        interest_theme_seqs=request.interest_theme_seqs,
    )

    redirect_response = RedirectResponse(url=settings.CORS_ALLOWED_FRONTEND_URL)
    redirect_response.set_cookie(
        key=USER_TOKEN_COOKIE_KEY,
        value=user_token_value,
        httponly=True,
        max_age=USER_TOKEN_TTL_SECONDS,
        samesite="lax",
    )
    redirect_response.set_cookie(
        key="nickname",
        value=quote(account.nickname or "", safe=""),
        httponly=True,
        max_age=USER_TOKEN_TTL_SECONDS,
        samesite="lax",
    )
    redirect_response.set_cookie(
        key="email",
        value=account.email,
        httponly=True,
        max_age=USER_TOKEN_TTL_SECONDS,
        samesite="lax",
    )

    return redirect_response


@router.delete("")
async def delete_account(
    user_token: str = Cookie(..., alias="user_token"),
    usecase: DeleteAccountUseCase = Depends(get_delete_account_usecase),
):
    await usecase.execute(user_token_value=user_token)
    return {"message": "Account deleted successfully"}
