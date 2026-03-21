from app.domains.authentication.adapter.outbound.cache.temp_token_lookup_redis_adapter import TempTokenLookupRedisAdapter
from app.domains.authentication.application.usecase.get_temp_user_info_usecase import GetTempUserInfoUseCase
from app.infrastructure.cache.redis_client import get_redis_client


def get_temp_user_info_usecase() -> GetTempUserInfoUseCase:
    return GetTempUserInfoUseCase(
        temp_token_lookup=TempTokenLookupRedisAdapter(redis_client=get_redis_client()),
    )
