# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    # The models point to catalog.Product, so the catalog's tables must exist first.
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActivityState",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "product",
                    models.ForeignKey(
                        related_name="active_samples",
                        verbose_name="Product",
                        to="catalog.Product",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductSamplesRelation",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "product",
                    models.ForeignKey(
                        related_name="products", verbose_name="Product", to="catalog.Product", on_delete=models.CASCADE
                    ),
                ),
                (
                    "sample",
                    models.ForeignKey(
                        related_name="samples", verbose_name="Sample", to="catalog.Product", on_delete=models.CASCADE
                    ),
                ),
            ],
        ),
    ]
