# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-20 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20190920_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_by',
            field=models.IntegerField(),
        ),
    ]
