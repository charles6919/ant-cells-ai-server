from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status

from app.domains.authentication.application.response.authentication_me_response import AuthenticationMeResponse
from app.domains.authentication.application.usecase.get_user_info_usecase import GetUserInfoUseCase
from app.domains.authentication.di import get_user_info_usecase

router = APIRouter(prefix="/authentication", tags=["authentication"])


@router.get("/me", response_model=AuthenticationMeResponse)
async def get_me(
    temp_token: Optional[str] = Cookie(None, alias="temp_token"),
    user_token: Optional[str] = Cookie(None, alias="user_token"),
    usecase: GetUserInfoUseCase = Depends(get_user_info_usecase),
):
    if not temp_token and not user_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided",
        )

    return await usecase.execute(temp_token=temp_token, user_token=user_token)
