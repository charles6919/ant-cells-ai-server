from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.account.adapter.outbound.persistence.account_persistence_adapter import AccountPersistenceAdapter
from app.domains.board.adapter.outbound.cache.user_token_read_redis_adapter import UserTokenReadRedisAdapter
from app.domains.board.adapter.outbound.persistence.board_persistence_adapter import BoardPersistenceAdapter
from app.domains.board.application.usecase.create_board_usecase import CreateBoardUseCase
from app.domains.board.application.usecase.get_board_list_usecase import GetBoardListUseCase
from app.domains.board.application.usecase.get_board_usecase import GetBoardUseCase
from app.domains.board.application.usecase.delete_board_usecase import DeleteBoardUseCase
from app.domains.board.application.usecase.update_board_usecase import UpdateBoardUseCase
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.database.database import get_db_session


def get_create_board_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> CreateBoardUseCase:
    redis = get_redis_client()
    return CreateBoardUseCase(
        board_repository=BoardPersistenceAdapter(session=session),
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
    )


def get_board_list_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetBoardListUseCase:
    redis = get_redis_client()
    return GetBoardListUseCase(
        board_repository=BoardPersistenceAdapter(session=session),
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
        account_repository=AccountPersistenceAdapter(session=session),
    )


def get_board_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetBoardUseCase:
    redis = get_redis_client()
    return GetBoardUseCase(
        board_repository=BoardPersistenceAdapter(session=session),
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
        account_repository=AccountPersistenceAdapter(session=session),
    )


def get_update_board_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> UpdateBoardUseCase:
    redis = get_redis_client()
    return UpdateBoardUseCase(
        board_repository=BoardPersistenceAdapter(session=session),
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
        account_repository=AccountPersistenceAdapter(session=session),
    )


def get_delete_board_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> DeleteBoardUseCase:
    redis = get_redis_client()
    return DeleteBoardUseCase(
        board_repository=BoardPersistenceAdapter(session=session),
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
    )
