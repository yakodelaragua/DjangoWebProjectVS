# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-04-25 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category_text',
            field=models.CharField(default='No category', max_length=200),
            preserve_default=False,
        ),
    ]