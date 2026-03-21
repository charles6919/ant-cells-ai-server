from fastapi import APIRouter, Cookie, Depends

from app.domains.authentication.application.response.authentication_me_response import AuthenticationMeResponse
from app.domains.authentication.application.usecase.get_temp_user_info_usecase import GetTempUserInfoUseCase
from app.domains.authentication.di import get_temp_user_info_usecase

router = APIRouter(prefix="/authentication", tags=["authentication"])


@router.get("/me", response_model=AuthenticationMeResponse)
async def get_me(
    temp_token: str = Cookie(..., alias="temp_token"),
    usecase: GetTempUserInfoUseCase = Depends(get_temp_user_info_usecase),
):
    return await usecase.execute(temp_token=temp_token)
