# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-26 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Textbooks', '0007_remove_book_edition'),
    ]

    operations = [
        migrations.AddField(
            model_name='sells',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]