from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.board.application.port.board_repository_port import BoardRepositoryPort
from app.domains.board.domain.entity.board import Board
from app.domains.board.infrastructure.mapper.board_mapper import BoardMapper
from app.domains.board.infrastructure.orm.board_orm import BoardORM


class BoardPersistenceAdapter(BoardRepositoryPort):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, board: Board) -> Board:
        orm = BoardMapper.to_orm(board)
        print(f"[DEBUG][BoardPersistence] inserting board id={orm.id} account_id={orm.account_id!r}")
        self._session.add(orm)
        try:
            await self._session.commit()
            print(f"[DEBUG][BoardPersistence] commit ok")
        except Exception as e:
            print(f"[DEBUG][BoardPersistence] commit FAILED: {type(e).__name__}: {e}")
            raise
        await self._session.refresh(orm)
        return BoardMapper.to_entity(orm)

    async def find_paginated(self, page: int, size: int) -> tuple[list[Board], int]:
        offset = (page - 1) * size

        total_result = await self._session.execute(select(func.count()).select_from(BoardORM))
        total_count = total_result.scalar_one()

        result = await self._session.execute(
            select(BoardORM)
            .order_by(BoardORM.created_at.desc())
            .offset(offset)
            .limit(size)
        )
        orms = result.scalars().all()
        boards = [BoardMapper.to_entity(orm) for orm in orms]

        return boards, total_count

    async def find_by_id(self, board_id: str) -> Optional[Board]:
        result = await self._session.execute(
            select(BoardORM).where(BoardORM.id == board_id)
        )
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return BoardMapper.to_entity(orm)

    async def delete(self, board_id: str) -> None:
        result = await self._session.execute(
            select(BoardORM).where(BoardORM.id == board_id)
        )
        orm = result.scalar_one_or_none()
        await self._session.delete(orm)
        await self._session.commit()

    async def update(self, board: Board) -> Board:
        result = await self._session.execute(
            select(BoardORM).where(BoardORM.id == board.id)
        )
        orm = result.scalar_one_or_none()
        orm.title = board.title
        orm.content = board.content
        orm.updated_at = board.updated_at
        await self._session.commit()
        await self._session.refresh(orm)
        return BoardMapper.to_entity(orm)
