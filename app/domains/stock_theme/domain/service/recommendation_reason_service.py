class RecommendationReasonService:
    INSTRUCTIONS = (
        "당신은 방산주 투자 분석 어시스턴트입니다. "
        "주어진 종목명, 매칭된 키워드, 관련 테마를 바탕으로 "
        "왜 이 종목이 추천되었는지를 투자자가 이해하기 쉬운 한국어 자연어 문장 1~2개로 설명하세요. "
        "반드시 어떤 키워드가 어떤 테마와 연결되어 추천되었는지 언급하세요. "
        "설명 외의 다른 텍스트는 출력하지 마세요."
    )

    @staticmethod
    def build_prompt(
        stock_name: str,
        matched_keywords: list[str],
        stock_themes: list[str],
    ) -> str:
        keywords_str = ", ".join(matched_keywords)
        themes_str = ", ".join(stock_themes)
        return (
            f"종목명: {stock_name}\n"
            f"매칭된 키워드: {keywords_str}\n"
            f"종목 관련 테마: {themes_str}"
        )
