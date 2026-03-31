from typing import Optional

from fastapi import HTTPException, status

from app.domains.stock_theme.application.port.stock_theme_repository_port import StockThemeRepositoryPort
from app.domains.stock_theme.application.port.user_token_read_port import UserTokenReadPort
from app.domains.stock_theme.application.response.stock_theme_response import StockThemeItemResponse, StockThemeListResponse
from app.domains.stock_theme.domain.service.stock_theme_service import StockThemeService


class GetStockThemesUseCase:
    def __init__(
        self,
        stock_theme_repository: StockThemeRepositoryPort,
        user_token_read: UserTokenReadPort,
    ):
        self.stock_theme_repository = stock_theme_repository
        self.user_token_read = user_token_read

    async def execute(self, user_token: str, theme: Optional[str] = None) -> StockThemeListResponse:
        account_id = await self.user_token_read.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        stocks = await self.stock_theme_repository.find_all()

        if theme:
            stocks = StockThemeService.filter_by_theme(stocks, theme)

        return StockThemeListResponse(
            total=len(stocks),
            stocks=[
                StockThemeItemResponse(id=s.id, name=s.name, code=s.code, themes=s.themes)
                for s in stocks
            ],
        )
