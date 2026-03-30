import logging

import httpx

from app.infrastructure.config import get_settings
from app.infrastructure.external.llm_client_port import LLMClientPort

logger = logging.getLogger(__name__)

_RESPONSES_URL = "https://api.openai.com/v1/responses"
_MODEL = "gpt-4o-mini"


class OpenAILLMClient(LLMClientPort):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, prompt: str, instructions: str = "") -> str:
        if not self.api_key or not self.api_key.strip():
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict = {"model": _MODEL, "input": prompt}
        if instructions:
            payload["instructions"] = instructions

        logger.info("[LLM] 요청 전송 (model=%s, prompt 길이=%d자)", _MODEL, len(prompt))

        async with httpx.AsyncClient() as client:
            response = await client.post(
                _RESPONSES_URL,
                headers=headers,
                json=payload,
                timeout=30.0,
            )

        logger.info("[LLM] 응답 상태 코드: %d", response.status_code)

        if response.status_code != 200:
            logger.error("[LLM] 요청 실패 (상태: %d): %s", response.status_code, response.text)
            response.raise_for_status()

        return self._extract_text(response.json())

    @staticmethod
    def _extract_text(data: dict) -> str:
        output_text = data.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        parts: list[str] = []
        for item in data.get("output", []):
            if not isinstance(item, dict):
                continue
            for block in item.get("content", []):
                if not isinstance(block, dict):
                    continue
                text = block.get("text")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())

        result = "\n".join(parts).strip()
        if not result:
            raise ValueError("OpenAI Responses API에서 텍스트 출력을 찾을 수 없습니다")
        return result


def get_llm_client() -> LLMClientPort:
    settings = get_settings()
    return OpenAILLMClient(api_key=settings.OPENAI_API_KEY)
