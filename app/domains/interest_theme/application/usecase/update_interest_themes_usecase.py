from fastapi import HTTPException, status

from app.domains.interest_theme.application.port.theme_repository_port import ThemeRepositoryPort
from app.domains.interest_theme.application.port.user_interest_theme_repository_port import UserInterestThemeRepositoryPort
from app.domains.interest_theme.application.port.user_token_read_port import UserTokenReadPort
from app.domains.interest_theme.application.response.theme_response import MyInterestThemeResponse


class UpdateInterestThemesUseCase:
    def __init__(
        self,
        user_token_read: UserTokenReadPort,
        theme_repository: ThemeRepositoryPort,
        user_interest_theme_repository: UserInterestThemeRepositoryPort,
    ):
        self.user_token_read = user_token_read
        self.theme_repository = theme_repository
        self.user_interest_theme_repository = user_interest_theme_repository

    async def execute(self, user_token: str, theme_seqs: list[int]) -> MyInterestThemeResponse:
        account_id = await self.user_token_read.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        if theme_seqs:
            valid_seqs = await self.theme_repository.find_active_seqs()
            invalid_seqs = [seq for seq in theme_seqs if seq not in valid_seqs]
            if invalid_seqs:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid theme seqs: {invalid_seqs}",
                )

        await self.user_interest_theme_repository.delete_all_by_account_id(account_id)

        if theme_seqs:
            await self.user_interest_theme_repository.save_all(account_id, theme_seqs)

        return MyInterestThemeResponse(theme_seqs=theme_seqs)
