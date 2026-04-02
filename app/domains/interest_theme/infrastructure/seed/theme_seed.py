from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.interest_theme.infrastructure.orm.theme_orm import ThemeORM

SEED_DATA: list[dict] = [
    {"theme": "방산", "description": "방위산업 관련 종목 (한화에어로스페이스, LIG넥스원 등)"},
    {"theme": "반도체", "description": "반도체 설계·제조·장비 관련 종목 (삼성전자, SK하이닉스 등)"},
    {"theme": "2차전지", "description": "배터리·소재·장비 관련 종목 (LG에너지솔루션, 삼성SDI 등)"},
    {"theme": "바이오", "description": "제약·바이오텍·헬스케어 관련 종목 (삼성바이오로직스, 셀트리온 등)"},
    {"theme": "에너지", "description": "신재생에너지·원전·수소 관련 종목"},
    {"theme": "AI", "description": "인공지능·빅데이터·클라우드 관련 종목"},
    {"theme": "로봇", "description": "로봇·자동화·스마트팩토리 관련 종목"},
    {"theme": "자동차", "description": "완성차·자율주행·전기차 관련 종목"},
    {"theme": "조선", "description": "조선·해운·해양플랜트 관련 종목"},
    {"theme": "금융", "description": "은행·증권·보험·핀테크 관련 종목"},
]


async def seed_themes(session: AsyncSession) -> None:
    result = await session.execute(select(func.count()).select_from(ThemeORM))
    count = result.scalar()

    if count and count > 0:
        return

    now = datetime.utcnow()
    for item in SEED_DATA:
        session.add(ThemeORM(
            theme=item["theme"],
            description=item["description"],
            is_active=True,
            created_at=now,
            updated_at=now,
        ))

    await session.commit()
