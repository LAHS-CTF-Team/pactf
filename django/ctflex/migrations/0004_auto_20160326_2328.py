# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 03:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0003_auto_20160326_2320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='affiliation',
            new_name='school',
        ),
    ]
