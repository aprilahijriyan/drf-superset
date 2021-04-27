from django.urls import path

from .views import (
    AccountConfirm,
    ForgotPassword,
    Login,
    Register,
    ResetPassword,
    ResetPasswordVerify,
)

urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("account/confirm/<token>", AccountConfirm.as_view(), name="account_confirm"),
    path("forgot-password", ForgotPassword.as_view(), name="forgot_password"),
    path(
        "reset-password/verify/<token>",
        ResetPasswordVerify.as_view(),
        name="reset_password_verify",
    ),
    path("reset-password/<token>", ResetPassword.as_view(), name="reset_password"),
]
