from rest_framework.authentication import BaseAuthentication

from app.common.security.jwt import JWTProvider
from .security.credentials import UserCredential


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("AUTHORIZATION", "").split(" ")
        if len(auth) != 2:
            return None
        elif auth[0].upper() != "JWT":
            return None

        payload = JWTProvider().decode(auth[1])
        return UserCredential(**payload), auth[1]
