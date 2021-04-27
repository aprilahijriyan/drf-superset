from pathlib import Path

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.mail import send_mail as _send_mail
from django.template.loader import get_template


def send_mail(template, context={}, **kwds):
    if not template.endswith((".html", ".htm")):
        raise TypeError(f"invalid template name: {template}")

    t = get_template(Path("email") / template)
    html = t.render(context)
    text = BeautifulSoup(html, "html.parser").text
    kwds["from_email"] = settings.DEFAULT_FROM_EMAIL
    kwds["html_message"] = html
    kwds["message"] = text
    _send_mail(**kwds)


def send_email_login(context={}, **kwds):
    kwds.setdefault("subject", "Login Alert!")
    template = "login.html"
    send_mail(template, context, **kwds)


def send_email_registration(context={}, **kwds):
    kwds.setdefault("subject", "Registration")
    template = "register.html"
    send_mail(template, context, **kwds)


def send_email_forgot_password(context={}, **kwds):
    kwds.setdefault("subject", "Forgot Password")
    template = "forgot_password.html"
    send_mail(template, context, **kwds)


def send_email_password_changed(context={}, **kwds):
    kwds.setdefault("subject", "Password Changed")
    template = "password_changed.html"
    send_mail(template, context, **kwds)
