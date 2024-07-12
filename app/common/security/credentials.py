from app.auth.models import UserPermission


class UserCredential:
    def __init__(self, pk: int, email: str, permission: str, **kwargs):
        self._pk = pk
        self._email = email
        self._permission = permission
        self._extra = kwargs

    @property
    def is_authenticated(self):
        return self._permission in (
            UserPermission.NORMAL,
            UserPermission.ADMIN,
            UserPermission.MASTER,
        )

    @property
    def pk(self) -> int:
        return self._pk

    @property
    def id(self) -> int:
        return self._pk

    @property
    def email(self) -> str:
        return self._email

    @property
    def permission(self) -> UserPermission:
        return UserPermission[self._permission]
