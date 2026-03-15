from fastapi import APIRouter, Depends, status

from app.domains.post.application.request.create_post_request import CreatePostRequest
from app.domains.post.application.response.create_post_response import CreatePostResponse
from app.domains.post.application.usecase.create_authenticated_post_usecase import CreateAuthenticatedPostUseCase
from app.domains.post.application.usecase.create_post_usecase import CreatePostUseCase
from app.domains.post.di import get_create_authenticated_post_usecase, get_create_post_usecase
from app.infrastructure.auth.current_user import get_current_user_id

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    request: CreatePostRequest,
    usecase: CreatePostUseCase = Depends(get_create_post_usecase),
):
    return await usecase.execute(request)


@router.post("/me", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create_authenticated_post(
    request: CreatePostRequest,
    user_id: str = Depends(get_current_user_id),
    usecase: CreateAuthenticatedPostUseCase = Depends(get_create_authenticated_post_usecase),
):
    return await usecase.execute(request, user_id)
