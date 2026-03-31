class MarketContextBuilderService:
    @staticmethod
    def build(stocks: list[dict]) -> str:
        """
        종목/테마 데이터를 LLM 프롬프트에 주입할 컨텍스트 문자열로 변환한다.

        stocks: [{"name": str, "code": str, "themes": list[str]}, ...]
        """
        if not stocks:
            return "현재 등록된 방산주 종목이 없습니다."

        lines = []
        for s in stocks:
            themes_str = ", ".join(s["themes"])
            lines.append(f"- {s['name']} ({s['code']}): 관련 테마 [{themes_str}]")

        return "\n".join(lines)
