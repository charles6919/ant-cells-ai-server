from pydantic import BaseModel


class UpdateInterestThemesRequest(BaseModel):
    theme_seqs: list[int]
