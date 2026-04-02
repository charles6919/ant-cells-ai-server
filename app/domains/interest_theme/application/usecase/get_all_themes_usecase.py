from app.domains.interest_theme.application.port.theme_repository_port import ThemeRepositoryPort
from app.domains.interest_theme.application.response.theme_response import ThemeItemResponse, ThemeListResponse


class GetAllThemesUseCase:
    def __init__(self, theme_repository: ThemeRepositoryPort):
        self.theme_repository = theme_repository

    async def execute(self) -> ThemeListResponse:
        themes = await self.theme_repository.find_all_active()
        return ThemeListResponse(
            total=len(themes),
            themes=[
                ThemeItemResponse(
                    seq=t.seq,
                    theme=t.theme,
                    description=t.description,
                )
                for t in themes
            ],
        )
