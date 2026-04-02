from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.domains.post.infrastructure.orm.post_orm import Base


class ThemeORM(Base):
    __tablename__ = "themes"

    seq = Column(Integer, primary_key=True, autoincrement=True)
    theme = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
