from dataclasses import dataclass
from typing import List


@dataclass
class AnalysisResult:
    keywords: List[str]
    sentiment: str
    sentiment_score: float
