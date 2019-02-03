from django.db import models
from django.utils.translation import ugettext_lazy as _


class Fuel(models.Model):
    """Fuel list."""
    "   id: the primary key"
    "   name: the fuel name"

    name = models.CharField(verbose_name=_("Nom"), max_length=255)

    class Meta:
        verbose_name = _("Carburant")

    def __str__(self):
        return self.name
