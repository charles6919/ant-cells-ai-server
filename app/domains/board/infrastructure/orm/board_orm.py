from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text

from app.domains.post.infrastructure.orm.post_orm import Base


class BoardORM(Base):
    __tablename__ = "boards"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    account_id = Column(String(36), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
