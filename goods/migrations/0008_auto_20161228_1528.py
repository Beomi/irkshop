# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 06:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_order_custom_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Order'),
        ),
    ]
