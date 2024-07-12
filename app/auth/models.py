from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserPermission(models.TextChoices):
    ANONYMOUS = ("ANONYMOUS", "비회원")
    NORMAL = ("NORMAL", "일반 회원")
    ADMIN = ("ADMIN", "관리자")
    MASTER = ("MASTER", "마스터")


class AuthUser(AbstractBaseUser):
    email = models.CharField(max_length=200, unique=True)
    permission = models.CharField(
        max_length=20,
        choices=UserPermission.choices,
        default=UserPermission.NORMAL,
    )
    is_active = models.BooleanField(default=True)
    created_dtm = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "tb_auth_user"
