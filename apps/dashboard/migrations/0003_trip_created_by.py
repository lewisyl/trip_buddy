# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-20 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20190920_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='created_by',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
