# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0017_auto_20170912_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='how_to_receive_krw',
            field=models.CharField(blank=True, choices=[('f', '현장수령'), ('l', '뒷풀이수령'), ('s', '배송(한국)')], max_length=1, null=True, verbose_name='(한국)수령방법'),
        ),
    ]
