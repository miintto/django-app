from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field

from app.auth.models import AuthUser


class UserByEmail:
    requires_context = True

    def __call__(self, serializer_field):
        try:
            return AuthUser.objects.get(
                email=serializer_field.root.initial_data["email"]
            )
        except AuthUser.DoesNotExist:
            raise ValidationError("Invalid Email!")


class UserFromRequestField(Field):
    def get_value(self, dictionary):
        assert "request" in self.context, "request is required in the context."
        try:
            return AuthUser.objects.get(pk=self.context["request"].user.id)
        except AuthUser.DoesNotExist:
            raise ValidationError("Invalid Email!")

    def to_internal_value(self, data):
        return data
