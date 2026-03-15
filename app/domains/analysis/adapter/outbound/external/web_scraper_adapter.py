import logging

import httpx
from bs4 import BeautifulSoup

from app.domains.analysis.application.port.article_content_port import ArticleContentPort

logger = logging.getLogger(__name__)


class WebScraperAdapter(ArticleContentPort):
    async def fetch_content(self, url: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.9",
                    },
                    follow_redirects=True,
                    timeout=15.0,
                )
                response.raise_for_status()
        except httpx.TimeoutException:
            raise RuntimeError(f"기사 URL 요청 시간 초과: {url}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"기사 URL 응답 오류 (HTTP {e.response.status_code}): {url}")
        except httpx.HTTPError as e:
            raise RuntimeError(f"기사 URL 요청 실패 ({type(e).__name__}): {url}")

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        return text
