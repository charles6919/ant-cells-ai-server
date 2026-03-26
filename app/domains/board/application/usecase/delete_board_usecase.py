from fastapi import HTTPException, status

from app.domains.board.application.port.board_repository_port import BoardRepositoryPort
from app.domains.board.application.port.user_token_read_port import UserTokenReadPort


class DeleteBoardUseCase:

    def __init__(
        self,
        board_repository: BoardRepositoryPort,
        user_token_read: UserTokenReadPort,
    ):
        self.board_repository = board_repository
        self.user_token_read = user_token_read

    async def execute(self, user_token: str, board_id: str) -> dict:
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

        await self.board_repository.delete(board_id)
        return {"message": "Board deleted successfully"}
