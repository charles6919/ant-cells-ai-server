from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.market_video.adapter.outbound.cache.user_token_read_redis_adapter import UserTokenReadRedisAdapter
from app.domains.market_video.adapter.outbound.external.kiwi_noun_extractor_adapter import KiwiNounExtractorAdapter
from app.domains.market_video.adapter.outbound.persistence.user_interest_theme_read_adapter import UserInterestThemeReadAdapter
from app.domains.market_video.adapter.outbound.external.youtube_channel_adapter import YouTubeChannelAdapter
from app.domains.market_video.adapter.outbound.external.youtube_comment_adapter import YouTubeCommentAdapter
from app.domains.market_video.adapter.outbound.external.youtube_search_adapter import YouTubeSearchAdapter
from app.domains.market_video.adapter.outbound.persistence.comment_persistence_adapter import CommentPersistenceAdapter
from app.domains.market_video.adapter.outbound.persistence.video_persistence_adapter import VideoPersistenceAdapter
from app.domains.market_video.application.usecase.collect_and_save_videos_usecase import CollectAndSaveVideosUseCase
from app.domains.market_video.application.usecase.collect_video_comments_usecase import CollectVideoCommentsUseCase
from app.domains.market_video.application.usecase.extract_nouns_usecase import ExtractNounsUseCase
from app.domains.market_video.application.usecase.get_video_list_usecase import GetVideoListUseCase
from app.domains.market_video.application.usecase.save_video_comments_usecase import SaveVideoCommentsUseCase
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db_session


def get_video_list_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetVideoListUseCase:
    redis = get_redis_client()
    return GetVideoListUseCase(
        video_repository=VideoPersistenceAdapter(session=session),
        user_token_read=UserTokenReadRedisAdapter(redis_client=redis),
        user_interest_theme_read=UserInterestThemeReadAdapter(session=session),
    )


def get_collect_and_save_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> CollectAndSaveVideosUseCase:
    settings = get_settings()
    return CollectAndSaveVideosUseCase(
        youtube_channel=YouTubeChannelAdapter(api_key=settings.YOUTUBE_API_KEY),
        video_repository=VideoPersistenceAdapter(session=session),
    )


def get_collect_video_comments_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> CollectVideoCommentsUseCase:
    settings = get_settings()
    return CollectVideoCommentsUseCase(
        youtube_comment=YouTubeCommentAdapter(api_key=settings.YOUTUBE_API_KEY),
        video_repository=VideoPersistenceAdapter(session=session),
    )


def get_save_video_comments_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> SaveVideoCommentsUseCase:
    settings = get_settings()
    return SaveVideoCommentsUseCase(
        youtube_comment=YouTubeCommentAdapter(api_key=settings.YOUTUBE_API_KEY),
        video_repository=VideoPersistenceAdapter(session=session),
        comment_repository=CommentPersistenceAdapter(session=session),
    )


def get_extract_nouns_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> ExtractNounsUseCase:
    return ExtractNounsUseCase(
        comment_repository=CommentPersistenceAdapter(session=session),
        noun_extractor=KiwiNounExtractorAdapter(),
    )
