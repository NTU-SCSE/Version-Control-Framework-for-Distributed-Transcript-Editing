# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 09:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdls', '0007_auto_20160308_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='is_assigned',
        ),
    ]
