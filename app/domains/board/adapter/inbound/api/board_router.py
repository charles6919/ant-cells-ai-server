from fastapi import APIRouter, Cookie, Depends, HTTPException, status

from app.domains.board.application.request.create_board_request import CreateBoardRequest
from app.domains.board.application.request.update_board_request import UpdateBoardRequest
from app.domains.board.application.response.board_list_response import BoardListResponse
from app.domains.board.application.response.board_read_response import BoardReadResponse
from app.domains.board.application.response.create_board_response import CreateBoardResponse
from app.domains.board.application.response.update_board_response import UpdateBoardResponse
from app.domains.board.application.usecase.create_board_usecase import CreateBoardUseCase
from app.domains.board.application.usecase.get_board_list_usecase import GetBoardListUseCase
from app.domains.board.application.usecase.get_board_usecase import GetBoardUseCase
from app.domains.board.application.usecase.delete_board_usecase import DeleteBoardUseCase
from app.domains.board.application.usecase.update_board_usecase import UpdateBoardUseCase
from app.domains.board.di import get_board_list_usecase, get_board_usecase, get_create_board_usecase, get_delete_board_usecase, get_update_board_usecase

router = APIRouter(prefix="/board", tags=["board"])


@router.post("/register", response_model=CreateBoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    request: CreateBoardRequest,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: CreateBoardUseCase = Depends(get_create_board_usecase),
):
    return await usecase.execute(user_token=user_token, request=request)


@router.get("/list", response_model=BoardListResponse)
async def get_board_list(
    page: int = 1,
    size: int = 10,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: GetBoardListUseCase = Depends(get_board_list_usecase),
):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page must be >= 1")
    if size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="size must be >= 1")

    return await usecase.execute(user_token=user_token, page=page, size=size)


@router.get("/read/{board_id}", response_model=BoardReadResponse)
async def get_board(
    board_id: str,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: GetBoardUseCase = Depends(get_board_usecase),
):
    return await usecase.execute(user_token=user_token, board_id=board_id)


@router.put("/edit/{board_id}", response_model=UpdateBoardResponse)
async def update_board(
    board_id: str,
    request: UpdateBoardRequest,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: UpdateBoardUseCase = Depends(get_update_board_usecase),
):
    return await usecase.execute(user_token=user_token, board_id=board_id, request=request)


@router.delete("/delete/{board_id}")
async def delete_board(
    board_id: str,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: DeleteBoardUseCase = Depends(get_delete_board_usecase),
):
    return await usecase.execute(user_token=user_token, board_id=board_id)
