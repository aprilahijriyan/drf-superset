from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Media(models.Model):
    title = models.CharField(_("title"), max_length=255)
    description = models.CharField(_("description"), max_length=255)
    link = models.ImageField(upload_to="avatar/", default=None, blank=True, null=True)
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=True, blank=True, null=True
    )
