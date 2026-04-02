from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.interest_theme.infrastructure.orm.theme_orm import ThemeORM
from app.domains.interest_theme.infrastructure.orm.user_interest_theme_orm import UserInterestThemeORM
from app.domains.market_video.application.port.user_interest_theme_read_port import UserInterestThemeReadPort


class UserInterestThemeReadAdapter(UserInterestThemeReadPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_theme_names_by_account_id(self, account_id: str) -> list[str]:
        result = await self.session.execute(
            select(ThemeORM.theme)
            .join(UserInterestThemeORM, ThemeORM.seq == UserInterestThemeORM.theme_seq)
            .where(UserInterestThemeORM.account_id == account_id)
        )
        return list(result.scalars().all())
