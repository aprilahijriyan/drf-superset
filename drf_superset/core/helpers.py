import random
import string
from datetime import timedelta
from uuid import uuid4

from django.http.request import HttpRequest
from django.urls import reverse

from .fernet import encrypt


def generate_random_string(length, chars=string.ascii_letters + string.digits):
    rv = ""
    while len(rv) != length:
        c = random.choice(chars)
        rv += c
    return rv


def generate_token(exp: timedelta = timedelta(hours=4)):
    data = encrypt(str(uuid4()).encode(), exp)
    return data


def absolute_url(request: HttpRequest, view: str, **kwagrs):
    """
    Reference: https://stackoverflow.com/questions/2345708/how-can-i-get-the-full-absolute-url-with-domain-in-django
    """

    uri = request.build_absolute_uri(reverse(view, **kwagrs))
    return uri
