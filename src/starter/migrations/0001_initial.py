# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-24 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=300, null=True)),
                ('last_name', models.CharField(blank=True, max_length=300, null=True)),
                ('message', models.CharField(max_length=300)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
    ]
