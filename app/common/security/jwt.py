from datetime import timedelta
import time

from django.conf import settings
from django.utils import timezone
import jwt

from app.auth.models import AuthUser


class JWTProvider:
    JWT_EXPIRATION = timedelta(hours=12)
    JWT_SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = "HS256"

    def encode(self, user: AuthUser) -> str:
        now = timezone.now()
        payload = {
            "pk": user.pk,
            "email": user.get_username(),
            "permission": user.permission,
            "exp": int(time.mktime((now + self.JWT_EXPIRATION).timetuple())),
            "iat": int(time.mktime(now.timetuple())),
        }
        return jwt.encode(
            payload=payload, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM
        )

    def decode(self, token: str) -> dict:
        return jwt.decode(
            jwt=token, key=self.JWT_SECRET_KEY, algorithms=self.ALGORITHM
        )
