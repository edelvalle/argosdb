from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from people.models import Discoverer


class BaseTree(MPTTModel):

    class MPTTMeta:
        order_insertion_by = ('name',)

    class Meta:
        abstract = True

    def __str__(self):
        names = (
            self
            .get_ancestors(include_self=True)
            .values_list('name', flat=True)
        )
        return ' > '.join(names)


class Material(BaseTree):

    name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('name'),
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name=_('parent'),
    )


class Decoration(BaseTree):

    name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('name')
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name=_('parent'),
    )


class Color(models.Model):

    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Finding(models.Model):
    date = models.DateField(db_index=True, verbose_name=_('date'))
    place = models.CharField(max_length=128, db_index=True)
    discoverers = models.ManyToManyField(Discoverer, related_name='findings')

    def __str__(self):
        from django.utils.translation import ugettext as _
        return _('{discoverers} at {place} on {date}').format(
            discoverers=', '.join(map(str, self.discoverers.all())),
            place=self.place,
            date=self.date,
        )


class Artifact(models.Model):

    name = models.CharField(
        max_length=1024,
        db_index=True,
        verbose_name=_('name'),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )

    main_material = models.ForeignKey(
        Material,
        related_name='artifacts',
        verbose_name=_('main material'),
    )

    colors = models.ManyToManyField(
        Color,
        blank=True,
        related_name='artifacts',
        verbose_name=_('colors'),
    )

    decorations = models.ManyToManyField(
        Decoration,
        blank=True,
        related_name='artifacts',
        verbose_name=_('decorations'),
    )

    found = models.ForeignKey(Finding)

    def __str__(self):
        return self.name
