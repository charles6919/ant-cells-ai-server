from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String

from app.domains.post.infrastructure.orm.post_orm import Base


class AccountORM(Base):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    kakao_id = Column(BigInteger, nullable=True, unique=True)
    nickname = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
