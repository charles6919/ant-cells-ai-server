from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.domains.market_analysis.application.port.llm_analysis_port import LLMAnalysisPort

_MODEL = "gpt-5-mini"

_SYSTEM_TEMPLATE = """당신은 방산주 전문 투자 분석 어시스턴트입니다.

아래는 현재 DB에 등록된 방산주 종목과 테마 정보입니다:

{context}

위 정보를 바탕으로 사용자의 질문에 한국어로 답변하세요.
방산 도메인과 무관한 질문(예: 일반 주식, IT, 음식, 스포츠 등)에는 반드시
"이 서비스는 방산주 관련 질문만 답변할 수 있습니다."라고만 답변하세요."""


class LangChainAnalysisAdapter(LLMAnalysisPort):
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def analyze(self, question: str, context: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", _SYSTEM_TEMPLATE),
            ("human", "{question}"),
        ])

        llm = ChatOpenAI(model=_MODEL, api_key=self._api_key)
        chain = prompt | llm | StrOutputParser()

        return await chain.ainvoke({"context": context, "question": question})
