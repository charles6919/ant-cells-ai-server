from dataclasses import dataclass


@dataclass
class StockTheme:
    id: int
    name: str
    code: str
    themes: list[str]
