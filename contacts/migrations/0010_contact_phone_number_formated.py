# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_auto_20171207_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='phone_number_formated',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
