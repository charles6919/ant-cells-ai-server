from app.domains.stock_theme.domain.entity.stock_theme import StockTheme


class StockThemeService:
    @staticmethod
    def filter_by_theme(stocks: list[StockTheme], theme: str) -> list[StockTheme]:
        """특정 테마 키워드에 해당하는 종목만 반환한다."""
        return [s for s in stocks if theme in s.themes]
