# Configuration

Default configuration on our boilerplate:

``` python
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "drf_superset.error_handler.handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "drf_superset.authentication.TokenAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": "a0d30aa8a4de89e3e24f7c2c980014869d9db6e21b64d16c34",
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "identity",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

AUTHENTICATION_BACKENDS = ["drf_superset.backends.EmailBackend"]

AUTH_USER_MODEL = "drf_superset.User"

# rfc: https://docs.djangoproject.com/id/3.2/topics/email/#smtp-backend
EMAIL_HOST = "localhost"
EMAIL_PORT = 8025
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

# rfc: https://docs.djangoproject.com/id/3.2/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "me@aprila.dev"

TOKEN_RESET_PASSWORD_DELTA = timedelta(hours=1)

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "oauth2",
            "in": "header",
            "name": "Bearer",
            "flow": "password",
            "tokenUrl": "/api/login",
        }
    },
    "SECURITY_REQUIREMENTS": [],
}
```

# IMPORTANT

You have to change the `SIGNING_KEY` value in the `SIMPLE_JWT` configuration.
That key will be used to create JWT, so it is not recommended to use one key for multiple projects.

You only need to create a secret key via the command below:

```
python manage.py generate_secret_key
```

And put that key into the `SIGNING_KEY` configuration.
