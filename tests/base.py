from django.test.client import Client

from app.auth.models import AuthUser
from app.common.security.jwt import JWTProvider

jwt = JWTProvider()


class TestClient(Client):
    """인증시 세션 및 쿠키 대신 JWT 토큰을 사용하는 방식으로 변경"""

    AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"

    def _login(self, user: AuthUser, backend=None):
        self.defaults[self.AUTH_HEADER_NAME] = f"JWT {jwt.encode(user)}"

    def logout(self):
        self.defaults.pop(self.AUTH_HEADER_NAME, None)