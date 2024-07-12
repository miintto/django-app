from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.auth.models import AuthUser
from app.common.security.jwt import JWTProvider


class RegisterSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(required=True)

    class Meta:
        model = AuthUser
        fields = ("email", "password", "password_check")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_check"]:
            raise ValidationError("Mismatched Password!")
        attrs["password"] = make_password(attrs["password"])
        return attrs

    def create(self, validated_data) -> str:
        validated_data.pop("password_check")
        user = super().create(validated_data)
        return JWTProvider().encode(user)


class AuthUserByEmail:
    requires_context = True

    def __call__(self, serializer_field):
        try:
            return AuthUser.objects.get(
                email=serializer_field.root.initial_data["email"]
            )
        except AuthUser.DoesNotExist:
            raise ValidationError("Invalid Email!")


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    user = serializers.HiddenField(default=AuthUserByEmail())

    def validate(self, attrs):
        if not check_password(attrs["password"], attrs["user"].password):
            raise ValidationError("Invalid Password!")
        return attrs

    def save(self) -> str:
        user = self.validated_data["user"]
        user.last_login = timezone.localtime()
        user.save(update_fields=["last_login"])
        return JWTProvider().encode(user)
