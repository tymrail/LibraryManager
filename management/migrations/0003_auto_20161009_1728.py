# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20161009_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author_ids',
            field=models.ManyToManyField(related_name='book', to='management.Author'),
        ),
    ]