from pydantic import BaseModel, field_validator


class CreateBoardRequest(BaseModel):
    title: str
    content: str

    @field_validator("title", "content")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v
