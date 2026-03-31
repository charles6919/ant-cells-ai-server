from collections import defaultdict

from app.domains.market_video.domain.value_object.synonym_mapping import SynonymMapping


class SynonymMergeService:
    """동의어 및 유사어를 하나의 대표 키워드로 통합하고 빈도수를 합산한다."""

    @staticmethod
    def merge(
        ranked: list[tuple[str, int]],
        synonym_mapping: SynonymMapping,
    ) -> list[tuple[str, int]]:
        """
        빈도수 리스트를 받아 동의어를 대표 키워드로 통합하고 빈도수를 합산한다.

        Args:
            ranked: (키워드, 빈도수) 튜플 리스트 (내림차순 정렬 상태)
            synonym_mapping: 동의어 매핑 테이블

        Returns:
            동의어가 통합되고 빈도수가 합산된 (키워드, 빈도수) 튜플 리스트 (내림차순)
        """
        merged: dict[str, int] = defaultdict(int)

        for keyword, count in ranked:
            canonical = synonym_mapping.resolve(keyword)
            merged[canonical] += count

        return sorted(merged.items(), key=lambda x: x[1], reverse=True)
