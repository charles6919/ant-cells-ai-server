from app.domains.session.application.port.session_store_port import SessionStorePort


class DeleteSessionUseCase:
    def __init__(self, session_store: SessionStorePort):
        self.session_store = session_store

    async def execute(self, token: str) -> None:
        await self.session_store.delete(token)
