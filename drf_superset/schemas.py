from rest_framework import fields
from rest_framework.serializers import Serializer


class LoginSuccessSchema(Serializer):
    access_token = fields.CharField()


class ResponseSchema(Serializer):
    detail = fields.CharField()
    status = fields.IntegerField()
