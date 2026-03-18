from typing import Optional

from app.domains.session.application.port.session_store_port import SessionStorePort
from app.domains.session.application.response.session_response import SessionResponse


class GetSessionUseCase:
    def __init__(self, session_store: SessionStorePort):
        self.session_store = session_store

    async def execute(self, token: str) -> Optional[SessionResponse]:
        session = await self.session_store.find_by_token(token)
        if session is None:
            return None
        return SessionResponse(
            token=session.token,
            user_id=session.user_id,
            role=session.role,
            expires_at=session.expires_at,
        )
