# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-18 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_orderhistory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Shipping',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '카테고리', 'verbose_name_plural': '카테고리'},
        ),
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '상품', 'verbose_name_plural': '상품'},
        ),
        migrations.AlterModelOptions(
            name='goodsimage',
            options={'verbose_name': '상품 이미지', 'verbose_name_plural': '상품 이미지'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '주문건', 'verbose_name_plural': '주문건'},
        ),
        migrations.AlterModelOptions(
            name='orderdetail',
            options={'verbose_name': '주문상세', 'verbose_name_plural': '주문상세'},
        ),
        migrations.AlterModelOptions(
            name='orderhistory',
            options={'verbose_name': '주문내역', 'verbose_name_plural': '주문내역'},
        ),
        migrations.RemoveField(
            model_name='goods',
            name='size',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='weight',
        ),
        migrations.AddField(
            model_name='order',
            name='ingress_agent_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='ingress_mail',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='order',
            name='is_shipping',
            field=models.BooleanField(default=False),
        ),
    ]
