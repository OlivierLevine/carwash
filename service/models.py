from django.db import models
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    """Services list."""
    "   id: the primary key"
    "   name: the service name"

    name = models.CharField(verbose_name=_("Nom"), max_length=255)

    class Meta:
        verbose_name = _("Service")

    def __str__(self):
        return self.name
