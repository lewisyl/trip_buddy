# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-20 18:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='user',
            new_name='users',
        ),
    ]
