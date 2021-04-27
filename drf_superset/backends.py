from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .core.mailer import send_email_login


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if not user.confirmed:
                return None

        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                send_email_login({"email": user.email}, recipient_list=[user.email])
                return user

        return None
