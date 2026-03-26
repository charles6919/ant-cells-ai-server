from fastapi import HTTPException, status

from app.domains.board.application.port.board_repository_port import BoardRepositoryPort
from app.domains.board.application.port.user_token_read_port import UserTokenReadPort
from app.domains.board.application.request.create_board_request import CreateBoardRequest
from app.domains.board.application.response.create_board_response import CreateBoardResponse
from app.domains.board.domain.entity.board import Board


class CreateBoardUseCase:

    def __init__(
        self,
        board_repository: BoardRepositoryPort,
        user_token_read: UserTokenReadPort,
    ):
        self.board_repository = board_repository
        self.user_token_read = user_token_read

    async def execute(self, user_token: str, request: CreateBoardRequest) -> CreateBoardResponse:
        print(f"[DEBUG][CreateBoard] user_token={user_token[:8]}...")
        account_id = await self.user_token_read.get_account_id(user_token)
        print(f"[DEBUG][CreateBoard] resolved account_id={account_id!r}")
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        board = Board(
            title=request.title,
            content=request.content,
            account_id=account_id,
        )
        print(f"[DEBUG][CreateBoard] saving board id={board.id} account_id={board.account_id}")
        saved = await self.board_repository.save(board)
        print(f"[DEBUG][CreateBoard] saved ok board_id={saved.id}")

        return CreateBoardResponse(
            board_id=saved.id,
            title=saved.title,
            content=saved.content,
            account_id=saved.account_id,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
