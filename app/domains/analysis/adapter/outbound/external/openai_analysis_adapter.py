import json

import httpx

from app.domains.analysis.application.port.article_analysis_port import ArticleAnalysisPort
from app.domains.analysis.domain.entity.analysis_result import AnalysisResult


class OpenAIAnalysisAdapter(ArticleAnalysisPort):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def analyze(self, content: str) -> AnalysisResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an article analysis assistant. "
                        "Analyze the given article and return a JSON object with the following fields:\n"
                        '- "keywords": a list of up to 5 key keywords (strings) from the article\n'
                        '- "sentiment": one of "positive", "negative", or "neutral"\n'
                        '- "sentiment_score": a float between -1.0 (most negative) and 1.0 (most positive)\n'
                        "Return ONLY the JSON object, no other text."
                    ),
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            "temperature": 0.0,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()

        raw = data["choices"][0]["message"]["content"]
        parsed = json.loads(raw)

        return AnalysisResult(
            keywords=parsed["keywords"],
            sentiment=parsed["sentiment"],
            sentiment_score=float(parsed["sentiment_score"]),
        )
