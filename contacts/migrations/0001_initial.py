# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 19:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('full_name', models.CharField(max_length=254)),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(max_length=6)),
                ('street_address', models.CharField(max_length=254)),
                ('city', models.CharField(max_length=128)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=254)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
