from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from people.models import Discoverer


class Material(MPTTModel):

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

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Decoration(models.Model):

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

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Color(models.Model):

    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Finding(models.Model):
    date = models.DateField(db_index=True, verbose_name=_('date'))
    place = models.CharField(max_length=128, db_index=True)
    discoverers = models.ManyToManyField(Discoverer, related_name='findings')


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

    color = models.ManyToManyField(
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
