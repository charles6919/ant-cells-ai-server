from fastapi import FastAPI

from app.infrastructure.config import get_settings

settings = get_settings()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
