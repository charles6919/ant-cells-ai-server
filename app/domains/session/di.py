from app.domains.session.adapter.outbound.in_memory.redis_session_adapter import RedisSessionAdapter
from app.domains.session.application.usecase.create_session_usecase import CreateSessionUseCase
from app.domains.session.application.usecase.delete_session_usecase import DeleteSessionUseCase
from app.domains.session.application.usecase.get_session_usecase import GetSessionUseCase
from app.infrastructure.cache.redis_client import get_redis_client


def get_create_session_usecase() -> CreateSessionUseCase:
    return CreateSessionUseCase(session_store=RedisSessionAdapter(get_redis_client()))


def get_get_session_usecase() -> GetSessionUseCase:
    return GetSessionUseCase(session_store=RedisSessionAdapter(get_redis_client()))


def get_delete_session_usecase() -> DeleteSessionUseCase:
    return DeleteSessionUseCase(session_store=RedisSessionAdapter(get_redis_client()))
