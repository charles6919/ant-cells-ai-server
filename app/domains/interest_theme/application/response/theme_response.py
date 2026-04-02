from pydantic import BaseModel


class ThemeItemResponse(BaseModel):
    seq: int
    theme: str
    description: str


class ThemeListResponse(BaseModel):
    total: int
    themes: list[ThemeItemResponse]


class MyInterestThemeResponse(BaseModel):
    theme_seqs: list[int]
