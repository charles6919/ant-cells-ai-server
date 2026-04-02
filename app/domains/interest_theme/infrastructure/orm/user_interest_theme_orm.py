from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.domains.post.infrastructure.orm.post_orm import Base


class UserInterestThemeORM(Base):
    __tablename__ = "user_interest_themes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(36), nullable=False)
    theme_seq = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
