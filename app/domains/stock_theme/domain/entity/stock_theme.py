from dataclasses import dataclass


@dataclass
class StockTheme:
    name: str
    code: str
    themes: list[str]
