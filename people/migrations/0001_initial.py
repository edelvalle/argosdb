# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-12 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discoverer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='name')),
                ('last_name', models.CharField(blank=True, db_index=True, max_length=128, null=True, verbose_name='last name')),
                ('is_istitution', models.BooleanField(default=False)),
            ],
        ),
    ]