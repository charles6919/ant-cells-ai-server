from app.domains.account.domain.entity.account import Account
from app.domains.account.infrastructure.orm.account_orm import AccountORM


class AccountMapper:

    @staticmethod
    def to_entity(orm: AccountORM) -> Account:
        return Account(
            id=orm.id,
            email=orm.email,
            kakao_id=orm.kakao_id,
            nickname=orm.nickname,
            created_at=orm.created_at,
        )

    @staticmethod
    def to_orm(entity: Account) -> AccountORM:
        return AccountORM(
            id=entity.id,
            email=entity.email,
            kakao_id=entity.kakao_id,
            nickname=entity.nickname,
            created_at=entity.created_at,
        )
