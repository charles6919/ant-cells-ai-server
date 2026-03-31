from sqlalchemy import Column, Integer, JSON, String

from app.domains.post.infrastructure.orm.post_orm import Base


class StockThemeORM(Base):
    __tablename__ = "stock_themes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    code = Column(String(20), nullable=False, unique=True)
    themes = Column(JSON, nullable=False)
