from django.contrib.auth import authenticate
from rest_framework import fields
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(Serializer):
    username = fields.EmailField()
    password = PasswordField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs: dict):
        params = {"email": attrs["username"], "password": attrs["password"]}
        params["request"] = self.context["request"]
        user = authenticate(**params)
        if not user:
            raise AuthenticationFailed("Invalid email or password")

        refresh = self.get_token(user)
        data = {}
        # data['refresh'] = str(refresh)
        data["access_token"] = str(refresh.access_token)

        return data


class RegisterSerializer(Serializer):
    first_name = fields.CharField(max_length=150)
    last_name = fields.CharField(max_length=150)
    email = fields.EmailField()
    password = PasswordField(min_length=8, max_length=150)


class ForgotPasswordSerializer(Serializer):
    email = fields.EmailField()


class ResetPasswordSerializer(Serializer):
    password = PasswordField(min_length=8, max_length=150)


class LimitOffsetSerializer(Serializer):
    limit = fields.IntegerField(required=False)
    offset = fields.IntegerField(required=False)
