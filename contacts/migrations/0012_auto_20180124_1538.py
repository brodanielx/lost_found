# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-24 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0011_auto_20171229_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Updated'),
        ),
    ]
