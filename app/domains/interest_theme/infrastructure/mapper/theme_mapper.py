from app.domains.interest_theme.domain.entity.theme import Theme
from app.domains.interest_theme.infrastructure.orm.theme_orm import ThemeORM


class ThemeMapper:
    @staticmethod
    def to_entity(orm: ThemeORM) -> Theme:
        return Theme(
            seq=orm.seq,
            theme=orm.theme,
            description=orm.description,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
