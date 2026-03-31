from dataclasses import dataclass

from app.domains.stock_theme.domain.entity.stock_theme import StockTheme


@dataclass
class StockRecommendationResult:
    stock: StockTheme
    matched_keywords: list[str]
    relevance_score: int


class StockRecommendationService:
    @staticmethod
    def recommend(
        stocks: list[StockTheme],
        keyword_counts: dict[str, int],
    ) -> list[StockRecommendationResult]:
        """
        종목의 테마와 키워드를 매칭하여 관련성 점수를 산출한다.

        관련성 점수 = 매칭된 테마 키워드의 빈도수 합산
        """
        results: list[StockRecommendationResult] = []

        for stock in stocks:
            matched = [theme for theme in stock.themes if theme in keyword_counts]
            if not matched:
                continue

            score = sum(keyword_counts[theme] for theme in matched)
            results.append(
                StockRecommendationResult(
                    stock=stock,
                    matched_keywords=matched,
                    relevance_score=score,
                )
            )

        return sorted(results, key=lambda r: r.relevance_score, reverse=True)
