from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.stock_theme.infrastructure.orm.stock_theme_orm import StockThemeORM

SEED_DATA: list[dict] = [
    {"name": "한화에어로스페이스", "code": "012450", "themes": ["전투기", "미사일", "항공엔진"]},
    {"name": "LIG넥스원", "code": "079550", "themes": ["미사일", "방공", "유도무기"]},
    {"name": "한국항공우주(KAI)", "code": "047810", "themes": ["전투기", "항공", "헬리콥터"]},
    {"name": "한화시스템", "code": "272210", "themes": ["레이더", "전자전", "C4I"]},
    {"name": "현대로템", "code": "064350", "themes": ["전차", "장갑차", "철도"]},
    {"name": "풍산", "code": "103140", "themes": ["탄약", "포탄", "동"]},
    {"name": "한국화이바", "code": "014580", "themes": ["방탄", "복합소재", "함정"]},
    {"name": "퍼스텍", "code": "010820", "themes": ["유도무기", "정밀기계"]},
    {"name": "이오시스템", "code": "098660", "themes": ["광학", "정밀조준", "열상장비"]},
    {"name": "빅텍", "code": "030790", "themes": ["함정", "통신", "전자장비"]},
    {"name": "SNT모티브", "code": "064960", "themes": ["소화기", "탄약", "차량부품"]},
    {"name": "휴니드", "code": "005870", "themes": ["통신", "전자전", "지휘체계"]},
    {"name": "스페코", "code": "013810", "themes": ["함정", "잠수함", "해양방산"]},
    {"name": "오르비텍", "code": "046710", "themes": ["미사일", "유도무기", "정밀부품"]},
    {"name": "한양이엔지", "code": "045100", "themes": ["방산시설", "군용인프라"]},
    {"name": "파워로직스", "code": "047310", "themes": ["드론", "배터리", "전자장비"]},
    {"name": "한국전자기술", "code": "072130", "themes": ["레이더", "전자장비", "방공"]},
    {"name": "세아제강", "code": "306200", "themes": ["탄약", "강관", "소재"]},
    {"name": "삼양컴텍", "code": "009730", "themes": ["장갑차", "차량", "방호소재"]},
    {"name": "포스코DX", "code": "022100", "themes": ["방산IT", "스마트팩토리"]},
]


async def seed_stock_themes(session: AsyncSession) -> None:
    """stock_themes 테이블이 비어 있으면 초기 방산주 데이터를 삽입한다."""
    from sqlalchemy import select, func

    result = await session.execute(select(func.count()).select_from(StockThemeORM))
    count = result.scalar()

    if count and count > 0:
        return

    import json
    from datetime import datetime

    for item in SEED_DATA:
        session.add(StockThemeORM(
            name=item["name"],
            code=item["code"],
            themes=json.dumps(item["themes"], ensure_ascii=False),
            created_at=datetime.now(),
        ))

    await session.commit()
