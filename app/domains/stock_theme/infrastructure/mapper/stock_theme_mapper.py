from app.domains.stock_theme.domain.entity.stock_theme import StockTheme
from app.domains.stock_theme.infrastructure.orm.stock_theme_orm import StockThemeORM


class StockThemeMapper:
    @staticmethod
    def to_entity(orm: StockThemeORM) -> StockTheme:
        import json
        themes = json.loads(orm.themes) if isinstance(orm.themes, str) and orm.themes else orm.themes or []
        return StockTheme(
            name=orm.name,
            code=orm.code,
            themes=themes,
        )

    @staticmethod
    def to_orm(entity: StockTheme) -> StockThemeORM:
        import json
        return StockThemeORM(
            name=entity.name,
            code=entity.code,
            themes=json.dumps(entity.themes, ensure_ascii=False),
        )
