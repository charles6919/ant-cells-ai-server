from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.post.adapter.outbound.persistence.post_repository_impl import PostRepositoryImpl
from app.domains.post.application.port.post_repository_port import PostRepositoryPort
from app.domains.post.application.usecase.create_authenticated_post_usecase import CreateAuthenticatedPostUseCase
from app.domains.post.application.usecase.create_post_usecase import CreatePostUseCase
from app.infrastructure.database.database import get_db_session


def get_post_repository(
    session: AsyncSession = Depends(get_db_session),
) -> PostRepositoryPort:
    return PostRepositoryImpl(session=session)


def get_create_post_usecase(
    post_repository: PostRepositoryPort = Depends(get_post_repository),
) -> CreatePostUseCase:
    return CreatePostUseCase(post_repository=post_repository)


def get_create_authenticated_post_usecase(
    post_repository: PostRepositoryPort = Depends(get_post_repository),
) -> CreateAuthenticatedPostUseCase:
    return CreateAuthenticatedPostUseCase(post_repository=post_repository)
