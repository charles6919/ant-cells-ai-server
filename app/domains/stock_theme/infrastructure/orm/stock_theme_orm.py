from sqlalchemy import Column, DateTime, String

from app.domains.post.infrastructure.orm.post_orm import Base


class StockThemeORM(Base):
    __tablename__ = "stock_themes"

    code = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    themes = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False)
