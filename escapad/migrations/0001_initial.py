# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('git_url', models.URLField(unique=True)),
                ('git_name', models.CharField(blank=True, max_length=200, null=True)),
                ('git_username', models.CharField(blank=True, max_length=200, null=True)),
                ('last_compiled', models.DateTimeField(blank=True, null=True)),
                ('provider', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
