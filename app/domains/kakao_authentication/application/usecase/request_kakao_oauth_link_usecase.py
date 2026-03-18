from app.domains.kakao_authentication.application.port.kakao_oauth_port import KakaoOAuthPort
from app.domains.kakao_authentication.application.response.kakao_auth_url_response import KakaoAuthUrlResponse


class RequestKakaoOAuthLinkUseCase:
    def __init__(self, kakao_oauth: KakaoOAuthPort):
        self.kakao_oauth = kakao_oauth

    def execute(self) -> KakaoAuthUrlResponse:
        auth_url = self.kakao_oauth.build_auth_url()
        return KakaoAuthUrlResponse(
            url=auth_url.url,
            client_id=auth_url.client_id,
            redirect_uri=auth_url.redirect_uri,
            response_type=auth_url.response_type,
        )
