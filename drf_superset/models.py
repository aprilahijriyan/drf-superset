from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Permission(models.Model):
    name = models.CharField(_("name"), max_length=100, null=False)
    description = models.CharField(_("description"), max_length=255, null=False)

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name})"


class Role(models.Model):
    name = models.CharField(_("name"), max_length=100, null=False)
    description = models.CharField(_("description"), max_length=255, null=False)
    permissions = models.ManyToManyField(Permission, verbose_name=_("permissions"))

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name})"


class Log(models.Model):
    request_password_reset_date = models.DateTimeField(
        _("request password reset date"), null=True
    )
    password_change_date = models.DateTimeField(_("password change date"), null=True)


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    fullname = models.TextField(_("full name"), null=False)
    confirmation_token = models.CharField(
        _("confirmation token"), max_length=255, null=True
    )
    confirmed = models.BooleanField(_("confirmed"), default=False)
    confirmed_date = models.DateTimeField(_("confirmed date"), null=True)
    reset_password_key = models.CharField(
        _("reset password key"), max_length=255, null=True
    )
    reset_password_token = models.CharField(
        _("reset password token"), max_length=255, null=True
    )
    roles = models.ManyToManyField(Role, verbose_name=_("roles"))
    logs = models.ManyToManyField(Log, verbose_name=_("logs"))

    def __str__(self) -> str:
        return f"{type(self).__name__}(email={self.email})"
