from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .core import fernet
from .core.exceptions import TokenExpiredException
from .core.helpers import generate_random_string, generate_token
from .core.mailer import (
    send_email_forgot_password,
    send_email_password_changed,
    send_email_registration,
)
from .schemas import LoginSuccessSchema
from .serializers import (
    ForgotPasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
)


class Login(TokenObtainPairView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        tags=["jwt"], request_body=LoginSerializer, responses={200: LoginSuccessSchema}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class Register(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(tags=["jwt"], request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data["email"]
            first_name = data["first_name"]
            last_name = data["last_name"]
            username = first_name + last_name + generate_random_string(4)
            model = get_user_model()
            if model.objects.filter(email=email).exists():
                msg = {"detail": "Email already exists"}
                status = 403
            else:
                token = str(uuid4())
                user = model.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    confirmation_token=token,
                )
                user.set_password(data["password"])
                user.save()
                msg = {"detail": "User has been created"}
                status = 200
                send_email_registration(
                    {"email": email, "token": token}, recipient_list=[user.email]
                )
        else:
            msg = serializer.errors
            status = 422

        return Response(msg, status)


class AccountConfirm(APIView):
    @swagger_auto_schema(tags=["jwt"])
    def get(self, request, token):
        model = get_user_model()
        user = model.objects.filter(confirmation_token=token).first()
        if user and not user.confirmed:
            msg = {"detail": "Confirmed"}
            status = 200
            user.confirmation_token = None
            user.confirmed = True
            user.confirmed_date = datetime.utcnow()
            user.save()
        else:
            msg = {"detail": "Invalid token"}
            status = 403

        return Response(msg, status)


class ForgotPassword(APIView):
    serializer_class = ForgotPasswordSerializer

    @swagger_auto_schema(tags=["jwt"], request_body=ForgotPasswordSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data["email"]
            model = get_user_model()
            user = model.objects.filter(email=email).first()
            if user:
                create_token = False
                key = user.reset_password_key
                token = user.reset_password_token
                if key and token:
                    try:
                        fernet.decrypt(token.encode(), key.encode())
                    except TokenExpiredException:
                        create_token = True
                else:
                    create_token = True

                if create_token:
                    msg = {"detail": "Email requesting password reset was sent"}
                    status = 200
                    key, token = generate_token(settings.TOKEN_RESET_PASSWORD_DELTA)
                    key = key.decode()
                    token = token.decode()
                    user.reset_password_key = key
                    user.reset_password_token = token
                    user.save()
                    send_email_forgot_password(
                        {"email": user.email, "token": token},
                        recipient_list=[user.email],
                    )
                else:
                    msg = {
                        "detail": "You have requested it several times, please try again later."
                    }
                    status = 403
            else:
                msg = {"detail": "User not found"}
                status = 404

        else:
            msg = serializer.errors
            status = 422

        return Response(msg, status)


class ResetPasswordVerify(APIView):
    @swagger_auto_schema(tags=["jwt"])
    def get(self, request, token):
        model = get_user_model()
        user = model.objects.filter(reset_password_token=token).first()
        if user:
            key = user.reset_password_key.encode()
            token = user.reset_password_token.encode()
            try:
                fernet.decrypt(token, key)
            except TokenExpiredException:
                message = "Invalid token"
                status = 403
            else:
                message = "Ok"
                status = 200
        else:
            message = "Invalid token"
            status = 403

        return Response(
            {
                "detail": message,
            },
            status,
        )


class ResetPassword(APIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(tags=["jwt"], request_body=ResetPasswordSerializer)
    def post(self, request, token, *args, **kwds):
        model = get_user_model()
        user = model.objects.filter(reset_password_token=token).first()
        if user:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                key = user.reset_password_key.encode()
                token = token.encode()
                try:
                    fernet.decrypt(token, key)
                except TokenExpiredException:
                    msg = {"detail": "Invalid token"}
                    status = 403
                else:
                    user.reset_password_key = None
                    user.reset_password_token = None
                    user.set_password(data["password"])
                    user.save()
                    msg = {"detail": "Password has been changed"}
                    status = 200
                    send_email_password_changed(
                        {"email": user.email}, recipient_list=[user.email]
                    )
            else:
                msg = serializer.errors
                status = 422
        else:
            msg = {"detail": "Invalid token"}
            status = 403

        return Response(msg, status)
