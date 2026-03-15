from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, Index
from sqlalchemy.sql import func

from app.domains.post.infrastructure.orm.post_orm import Base


class SavedNewsORM(Base):
    __tablename__ = "saved_news"

    __table_args__ = (
        Index("idx_saved_news_link", "link", unique=True, mysql_length=255),
    )

    id = Column(String(36), primary_key=True)
    title = Column(String(500), nullable=False)
    link = Column(String(2048), nullable=False)
    source = Column(String(255), nullable=False, default="")
    published_at = Column(String(100), nullable=False, default="")
    snippet = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    saved_at = Column(DateTime, nullable=False, server_default=func.now())
