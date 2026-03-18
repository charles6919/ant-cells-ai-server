import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.domains.session.application.port.session_store_port import SessionStorePort
from app.domains.session.application.request.login_request import LoginRequest
from app.domains.session.application.response.session_response import SessionResponse
from app.domains.session.domain.entity.session_data import SessionData
from app.infrastructure.config import get_settings


class CreateSessionUseCase:
    def __init__(self, session_store: SessionStorePort):
        self.session_store = session_store

    async def execute(self, request: LoginRequest) -> SessionResponse:
        settings = get_settings()

        if request.auth_password != settings.AUTH_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid auth password",
            )

        token = secrets.token_urlsafe(32)
        now = datetime.utcnow()
        expires_at = now + timedelta(seconds=settings.SESSION_TTL_SECONDS)

        session = SessionData(
            token=token,
            user_id=request.user_id,
            role=request.role,
            created_at=now,
            expires_at=expires_at,
        )

        await self.session_store.save(session, ttl_seconds=settings.SESSION_TTL_SECONDS)

        return SessionResponse(
            token=token,
            user_id=session.user_id,
            role=session.role,
            expires_at=session.expires_at,
        )
