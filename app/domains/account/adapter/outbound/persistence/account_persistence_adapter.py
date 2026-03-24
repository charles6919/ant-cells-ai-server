from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.account.application.port.account_repository_port import AccountRepositoryPort
from app.domains.account.domain.entity.account import Account
from app.domains.account.infrastructure.mapper.account_mapper import AccountMapper
from app.domains.account.infrastructure.orm.account_orm import AccountORM


class AccountPersistenceAdapter(AccountRepositoryPort):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, account_id: str) -> Optional[Account]:
        result = await self._session.execute(
            select(AccountORM).where(AccountORM.id == account_id)
        )
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return AccountMapper.to_entity(orm)

    async def find_by_email(self, email: str) -> Optional[Account]:
        result = await self._session.execute(
            select(AccountORM).where(AccountORM.email == email)
        )
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return AccountMapper.to_entity(orm)

    async def save(self, account: Account) -> None:
        orm = AccountMapper.to_orm(account)
        self._session.add(orm)
        await self._session.commit()
