from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

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
    date = models.DateField(
        null=True, blank=True,
        db_index=True,
        verbose_name=_('date')
    )
    place = models.CharField(
        null=True, blank=True,
        db_index=True,
        max_length=128,
    )
    discoverers = models.ManyToManyField(
        Discoverer,
        blank=True,
        related_name='findings',
    )

    def __str__(self):
        from django.utils.translation import ugettext as _
        result = []
        if self.discoverers.exists():
            discoverers = ', '.join(map(str, self.discoverers.all()))
            result.append(_('by %s') % discoverers)
        if self.place:
            result.append(_('at %s') % self.place)
        if self.date:
            result.append(_('on %s') % self.date)
        return ' '.join(result)


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

    found = models.ForeignKey(
        Finding,
        null=True, blank=True,
        verbose_name=_('found by')
    )

    found_date = models.DateTimeField(db_index=True, null=True)

    def __str__(self):
        return self.name

    def get_colors(self):
        return ', '.join(self.colors.values_list('name', flat=True))
    get_colors.short_description = colors.verbose_name

    def save(self, *args, **kwargs):
        self.found_date = self.found and self.found.date
        return super().save(*args, **kwargs)


class Image(models.Model):
    artifact = models.ForeignKey(Artifact)

    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='artifacts/',
    )

    def admin_image(self):
        return format_html('<img src="{url}" width=250  />', url=self.image.url)
    admin_image.short_description = image.verbose_name
    admin_image.allow_tags = True
