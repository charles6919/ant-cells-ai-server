from app.domains.interest_theme.application.port.user_interest_theme_repository_port import UserInterestThemeRepositoryPort


class SaveUserInterestThemesUseCase:
    def __init__(self, user_interest_theme_repository: UserInterestThemeRepositoryPort):
        self.user_interest_theme_repository = user_interest_theme_repository

    async def execute(self, account_id: str, theme_seqs: list[int]) -> None:
        if not theme_seqs:
            return
        await self.user_interest_theme_repository.save_all(account_id, theme_seqs)
