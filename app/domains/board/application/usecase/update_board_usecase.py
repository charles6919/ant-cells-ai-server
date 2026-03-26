from fastapi import HTTPException, status

from app.domains.account.application.port.account_repository_port import AccountRepositoryPort
from app.domains.board.application.port.board_repository_port import BoardRepositoryPort
from app.domains.board.application.port.user_token_read_port import UserTokenReadPort
from app.domains.board.application.request.update_board_request import UpdateBoardRequest
from app.domains.board.application.response.update_board_response import UpdateBoardResponse


class UpdateBoardUseCase:

    def __init__(
        self,
        board_repository: BoardRepositoryPort,
        user_token_read: UserTokenReadPort,
        account_repository: AccountRepositoryPort,
    ):
        self.board_repository = board_repository
        self.user_token_read = user_token_read
        self.account_repository = account_repository

    async def execute(self, user_token: str, board_id: str, request: UpdateBoardRequest) -> UpdateBoardResponse:
        account_id = await self.user_token_read.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        board = await self.board_repository.find_by_id(board_id)
        if board is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found",
            )

        if board.account_id != account_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the author of this board",
            )

        board.update(title=request.title, content=request.content)
        updated = await self.board_repository.update(board)

        account = await self.account_repository.find_by_id(updated.account_id)
        nickname = account.nickname if account and account.nickname else "unknown"

        return UpdateBoardResponse(
            board_id=updated.id,
            title=updated.title,
            content=updated.content,
            nickname=nickname,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )
