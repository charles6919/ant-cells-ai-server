from abc import ABC, abstractmethod
from typing import Optional

from app.domains.board.domain.entity.board import Board


class BoardRepositoryPort(ABC):

    @abstractmethod
    async def save(self, board: Board) -> Board:
        pass

    @abstractmethod
    async def find_paginated(self, page: int, size: int) -> tuple[list[Board], int]:
        """Returns (boards, total_count) for the given page/size."""
        pass

    @abstractmethod
    async def find_by_id(self, board_id: str) -> Optional[Board]:
        pass

    @abstractmethod
    async def update(self, board: Board) -> Board:
        pass

    @abstractmethod
    async def delete(self, board_id: str) -> None:
        pass
