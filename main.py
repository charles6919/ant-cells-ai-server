from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.domains.account.adapter.inbound.api.register_router import router as register_router
from app.domains.authentication.adapter.inbound.api.authentication_router import router as authentication_router
from app.domains.analysis.adapter.inbound.api.analysis_router import router as analysis_router
from app.domains.news.adapter.inbound.api.news_router import router as news_router
from app.domains.post.adapter.inbound.api.post_router import router as post_router
from app.domains.kakao_authentication.adapter.inbound.api.kakao_authentication_router import router as kakao_authentication_router
from app.domains.session.adapter.inbound.api.session_router import router as session_router
from app.domains.board.adapter.inbound.api.board_router import router as board_router
from app.domains.market_video.adapter.inbound.api.market_video_router import router as market_video_router
from app.domains.stock_theme.adapter.inbound.api.stock_theme_router import router as stock_theme_router
from app.domains.market_analysis.adapter.inbound.api.market_analysis_router import router as market_analysis_router
from app.domains.account.infrastructure.orm.account_orm import AccountORM  # noqa: F401
from app.domains.news.infrastructure.orm.saved_news_orm import SavedNewsORM  # noqa: F401
from app.domains.board.infrastructure.orm.board_orm import BoardORM  # noqa: F401
from app.domains.market_video.infrastructure.orm.saved_video_orm import SavedVideoORM  # noqa: F401
from app.domains.market_video.infrastructure.orm.video_comment_orm import VideoCommentORM  # noqa: F401
from app.domains.stock_theme.infrastructure.orm.stock_theme_orm import StockThemeORM  # noqa: F401
from app.domains.post.infrastructure.orm.post_orm import Base
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import AsyncSessionLocal, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from app.domains.stock_theme.infrastructure.seed.stock_theme_seed import seed_stock_themes
    async with AsyncSessionLocal() as session:
        await seed_stock_themes(session)

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ALLOWED_FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register_router)
app.include_router(authentication_router)
app.include_router(post_router)
app.include_router(news_router)
app.include_router(analysis_router)
app.include_router(session_router)
app.include_router(kakao_authentication_router)
app.include_router(board_router)
app.include_router(market_video_router)
app.include_router(stock_theme_router)
app.include_router(market_analysis_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
