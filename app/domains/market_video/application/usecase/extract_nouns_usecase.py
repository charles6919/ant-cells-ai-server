from typing import Optional

from app.domains.market_video.application.port.comment_repository_port import CommentRepositoryPort
from app.domains.market_video.application.port.noun_extractor_port import NounExtractorPort
from app.domains.market_video.application.response.noun_frequency_response import NounFrequencyResponse, NounItemResponse
from app.domains.market_video.domain.service.noun_frequency_service import NounFrequencyService
from app.domains.market_video.domain.service.synonym_merge_service import SynonymMergeService
from app.domains.market_video.domain.value_object.synonym_mapping import SynonymMapping


class ExtractNounsUseCase:
    def __init__(
        self,
        comment_repository: CommentRepositoryPort,
        noun_extractor: NounExtractorPort,
    ):
        self.comment_repository = comment_repository
        self.noun_extractor = noun_extractor

    async def execute(self, video_id: Optional[str], top_n: int = 30) -> NounFrequencyResponse:
        if video_id:
            texts = await self.comment_repository.find_contents_by_video_id(video_id)
        else:
            texts = await self.comment_repository.find_all_contents()

        nouns = self.noun_extractor.extract_nouns(texts)
        ranked = NounFrequencyService.count_frequencies(nouns)
        merged = SynonymMergeService.merge(ranked, SynonymMapping())

        return NounFrequencyResponse(
            video_id=video_id or "all",
            total_comment_count=len(texts),
            total_noun_count=len(merged),
            top_n=top_n,
            nouns=[NounItemResponse(noun=noun, count=count) for noun, count in merged[:top_n]],
        )
