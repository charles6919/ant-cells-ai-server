from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domains.session.application.request.login_request import LoginRequest
from app.domains.session.application.response.session_response import SessionResponse
from app.domains.session.application.usecase.create_session_usecase import CreateSessionUseCase
from app.domains.session.application.usecase.delete_session_usecase import DeleteSessionUseCase
from app.domains.session.application.usecase.get_session_usecase import GetSessionUseCase
from app.domains.session.di import (
    get_create_session_usecase,
    get_delete_session_usecase,
    get_get_session_usecase,
)

router = APIRouter(prefix="/session", tags=["session"])

security = HTTPBearer()


@router.post("/login", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def login(
    request: LoginRequest,
    usecase: CreateSessionUseCase = Depends(get_create_session_usecase),
):
    return await usecase.execute(request)


@router.get("", response_model=Optional[SessionResponse])
async def get_session(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    usecase: GetSessionUseCase = Depends(get_get_session_usecase),
):
    session = await usecase.execute(credentials.credentials)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or expired",
        )
    return session


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    usecase: DeleteSessionUseCase = Depends(get_delete_session_usecase),
):
    await usecase.execute(credentials.credentials)
