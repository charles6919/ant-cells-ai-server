from abc import ABC, abstractmethod
from typing import Optional

from app.domains.market_video.domain.entity.saved_video import SavedVideo


class VideoRepositoryPort(ABC):
    @abstractmethod
    async def upsert(self, video: SavedVideo) -> SavedVideo:
        pass

    @abstractmethod
    async def find_all(self, page: int, size: int) -> tuple[list[SavedVideo], int]:
        """저장된 영상 목록을 게시일 내림차순으로 반환한다. (videos, total_count)"""
        pass

    @abstractmethod
    async def find_by_video_id(self, video_id: str) -> Optional[SavedVideo]:
        """video_id로 저장된 영상을 조회한다. 없으면 None을 반환한다."""
        pass

    @abstractmethod
    async def find_all_by_title_keywords(
        self, keywords: list[str], page: int, size: int,
    ) -> tuple[list[SavedVideo], int]:
        """제목에 키워드가 포함된 영상을 게시일 내림차순으로 반환한다."""
        pass

