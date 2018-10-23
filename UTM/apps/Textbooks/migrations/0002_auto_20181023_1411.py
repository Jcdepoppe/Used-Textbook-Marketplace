# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-23 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Textbooks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='sells',
            name='picture',
            field=models.ImageField(blank=True, default='No-pic.png', null=True, upload_to='user_pics/', verbose_name=''),
        ),
    ]