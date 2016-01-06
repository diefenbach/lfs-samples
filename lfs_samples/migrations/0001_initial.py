# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name='ActivityState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.ForeignKey(related_name='active_samples', verbose_name='Product', to='catalog.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSamplesRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.ForeignKey(related_name='products', verbose_name='Product', to='catalog.Product')),
                ('sample', models.ForeignKey(related_name='samples', verbose_name='Sample', to='catalog.Product')),
            ],
        ),
    ]
