# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-23 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0002_auto_20160223_0206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='a_id',
        ),
        migrations.AlterField(
            model_name='announcement',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]