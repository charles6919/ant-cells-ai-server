from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.interest_theme.application.port.user_interest_theme_repository_port import UserInterestThemeRepositoryPort
from app.domains.interest_theme.infrastructure.orm.theme_orm import ThemeORM
from app.domains.interest_theme.infrastructure.orm.user_interest_theme_orm import UserInterestThemeORM


class UserInterestThemePersistenceAdapter(UserInterestThemeRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_all(self, account_id: str, theme_seqs: list[int]) -> None:
        for theme_seq in theme_seqs:
            self.session.add(UserInterestThemeORM(
                account_id=account_id,
                theme_seq=theme_seq,
                created_at=datetime.utcnow(),
            ))
        await self.session.commit()

    async def find_theme_names_by_account_id(self, account_id: str) -> list[str]:
        result = await self.session.execute(
            select(ThemeORM.theme)
            .join(UserInterestThemeORM, ThemeORM.seq == UserInterestThemeORM.theme_seq)
            .where(UserInterestThemeORM.account_id == account_id)
        )
        return list(result.scalars().all())

    async def find_theme_seqs_by_account_id(self, account_id: str) -> list[int]:
        result = await self.session.execute(
            select(UserInterestThemeORM.theme_seq)
            .where(UserInterestThemeORM.account_id == account_id)
        )
        return list(result.scalars().all())

    async def delete_all_by_account_id(self, account_id: str) -> None:
        await self.session.execute(
            delete(UserInterestThemeORM)
            .where(UserInterestThemeORM.account_id == account_id)
        )
        await self.session.commit()
