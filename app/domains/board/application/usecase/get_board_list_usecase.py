import math

from fastapi import HTTPException, status

from app.domains.account.application.port.account_repository_port import AccountRepositoryPort
from app.domains.board.application.port.board_repository_port import BoardRepositoryPort
from app.domains.board.application.port.user_token_read_port import UserTokenReadPort
from app.domains.board.application.response.board_list_response import BoardItemResponse, BoardListResponse


class GetBoardListUseCase:

    def __init__(
        self,
        board_repository: BoardRepositoryPort,
        user_token_read: UserTokenReadPort,
        account_repository: AccountRepositoryPort,
    ):
        self.board_repository = board_repository
        self.user_token_read = user_token_read
        self.account_repository = account_repository

    async def execute(self, user_token: str, page: int, size: int) -> BoardListResponse:
        print(f"[DEBUG][GetBoardList] user_token={user_token[:8]}...")
        account_id = await self.user_token_read.get_account_id(user_token)
        print(f"[DEBUG][GetBoardList] resolved account_id={account_id!r}")
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        boards, total_count = await self.board_repository.find_paginated(page, size)
        print(f"[DEBUG][GetBoardList] fetched boards count={len(boards)} total={total_count}")

        items = []
        for board in boards:
            print(f"[DEBUG][GetBoardList] resolving nickname for board_id={board.id} account_id={board.account_id!r}")
            account = await self.account_repository.find_by_id(board.account_id)
            print(f"[DEBUG][GetBoardList] account={account!r}")
            nickname = account.nickname if account and account.nickname else "unknown"
            items.append(BoardItemResponse(
                board_id=board.id,
                title=board.title,
                content=board.content,
                nickname=nickname,
                created_at=board.created_at,
                updated_at=board.updated_at,
            ))

        total_pages = math.ceil(total_count / size) if size > 0 else 0

        return BoardListResponse(
            items=items,
            current_page=page,
            total_pages=total_pages,
            total_count=total_count,
        )
