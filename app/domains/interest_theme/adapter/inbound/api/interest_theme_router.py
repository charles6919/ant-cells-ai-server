from fastapi import APIRouter, Cookie, Depends

from app.domains.interest_theme.application.request.update_interest_themes_request import UpdateInterestThemesRequest
from app.domains.interest_theme.application.response.theme_response import MyInterestThemeResponse, ThemeListResponse
from app.domains.interest_theme.application.usecase.get_all_themes_usecase import GetAllThemesUseCase
from app.domains.interest_theme.application.usecase.get_my_interest_themes_usecase import GetMyInterestThemesUseCase
from app.domains.interest_theme.application.usecase.update_interest_themes_usecase import UpdateInterestThemesUseCase
from app.domains.interest_theme.di import get_all_themes_usecase, get_my_interest_themes_usecase, get_update_interest_themes_usecase

router = APIRouter(prefix="/themes", tags=["themes"])


@router.get("", response_model=ThemeListResponse)
async def get_all_themes(
    usecase: GetAllThemesUseCase = Depends(get_all_themes_usecase),
):
    return await usecase.execute()


@router.get("/me", response_model=MyInterestThemeResponse)
async def get_my_interest_themes(
    user_token: str = Cookie(..., alias="user_token"),
    usecase: GetMyInterestThemesUseCase = Depends(get_my_interest_themes_usecase),
):
    return await usecase.execute(user_token=user_token)


@router.put("/me", response_model=MyInterestThemeResponse)
async def update_my_interest_themes(
    request: UpdateInterestThemesRequest,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: UpdateInterestThemesUseCase = Depends(get_update_interest_themes_usecase),
):
    return await usecase.execute(user_token=user_token, theme_seqs=request.theme_seqs)
