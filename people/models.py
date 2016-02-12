from django.db import models
from django.utils.translation import ugettext_lazy as _


class Discoverer(models.Model):

    name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('name'))

    last_name = models.CharField(
        max_length=128,
        db_index=True,
        null=True, blank=True,
        verbose_name=_('last name')
    )

    is_istitution = models.BooleanField(default=False)

    def __str__(self):
        return '{0} {1}'.format(self.name, self.last_name or '').strip()
