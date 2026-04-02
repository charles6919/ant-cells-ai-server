from fastapi import HTTPException, status

from app.domains.interest_theme.application.port.user_interest_theme_repository_port import UserInterestThemeRepositoryPort
from app.domains.interest_theme.application.port.user_token_read_port import UserTokenReadPort
from app.domains.interest_theme.application.response.theme_response import MyInterestThemeResponse


class GetMyInterestThemesUseCase:
    def __init__(
        self,
        user_token_read: UserTokenReadPort,
        user_interest_theme_repository: UserInterestThemeRepositoryPort,
    ):
        self.user_token_read = user_token_read
        self.user_interest_theme_repository = user_interest_theme_repository

    async def execute(self, user_token: str) -> MyInterestThemeResponse:
        account_id = await self.user_token_read.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        theme_seqs = await self.user_interest_theme_repository.find_theme_seqs_by_account_id(account_id)
        return MyInterestThemeResponse(theme_seqs=theme_seqs)
