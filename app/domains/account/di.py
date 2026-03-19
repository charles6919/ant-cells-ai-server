from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.account.adapter.outbound.persistence.account_persistence_adapter import AccountPersistenceAdapter
from app.infrastructure.database.database import get_db_session


def get_account_persistence_adapter(
    session: AsyncSession = Depends(get_db_session),
) -> AccountPersistenceAdapter:
    return AccountPersistenceAdapter(session=session)
