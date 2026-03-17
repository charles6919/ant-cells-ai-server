from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.domains.news.application.request.save_news_request import SaveNewsRequest
from app.domains.news.application.request.search_news_request import SearchNewsRequest
from app.domains.news.application.response.save_news_response import SaveNewsResponse
from app.domains.news.application.response.search_news_response import SearchNewsResponse
from app.domains.news.application.usecase.save_news_usecase import SaveNewsUseCase
from app.domains.news.application.usecase.search_news_usecase import SearchNewsUseCase
from app.domains.news.di import get_save_news_usecase, get_search_news_usecase

router = APIRouter(prefix="/news", tags=["news"])


# GET 요청 <- 브라우저 입력
@router.get("/search", response_model=SearchNewsResponse)
async def search_news(
    # 검색어
    keyword: str = Query(..., min_length=1),
    # 디폴트로 첫 번째 페이지부터 보여줌
    page: int = Query(1, ge=1),
    # 디폴트로 10개씩 전달
    size: int = Query(10, ge=1, le=100),
    # Google Serp API에 대한 의존성 추가
    usecase: SearchNewsUseCase = Depends(get_search_news_usecase),
):
    request = SearchNewsRequest(keyword=keyword, page=page, size=size)
    # postman에서 get 요청을 했을 때 나왔던 결과가 결국 아래 파트의 return 응답
    return await usecase.execute(request)


@router.post("/saved", response_model=SaveNewsResponse, status_code=status.HTTP_201_CREATED)
async def save_news(
    # 무엇을 save 할 것인지에 대한 request 정보
    request: SaveNewsRequest,
    # 의존성 주입 (Dependency Injection) <- Service (Usecase)
    # application 패키지에서 찾으면 됩니다.
    usecase: SaveNewsUseCase = Depends(get_save_news_usecase),
):
    try:
        # 결론적으로 여기서 저장된 기사(뉴스)의 아이디 값을 반환함.
        return await usecase.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
