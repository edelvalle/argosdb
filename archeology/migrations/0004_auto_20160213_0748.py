# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-13 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archeology', '0003_artifact_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='artifacts/', verbose_name='image'),
        ),
    ]
