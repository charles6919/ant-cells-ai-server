from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.domains.analysis.adapter.inbound.api.analysis_router import router as analysis_router
from app.domains.news.adapter.inbound.api.news_router import router as news_router
from app.domains.post.adapter.inbound.api.post_router import router as post_router
from app.domains.kakao_authentication.adapter.inbound.api.kakao_authentication_router import router as kakao_authentication_router
from app.domains.session.adapter.inbound.api.session_router import router as session_router
from app.domains.news.infrastructure.orm.saved_news_orm import SavedNewsORM  # noqa: F401
from app.domains.post.infrastructure.orm.post_orm import Base
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
app.include_router(news_router)
app.include_router(analysis_router)
app.include_router(session_router)
app.include_router(kakao_authentication_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
