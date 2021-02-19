# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lfs_samples', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.ForeignKey(related_name='is_sample', verbose_name='Product', to='catalog.Product', on_delete=models.CASCADE)),
            ],
        ),
    ]
