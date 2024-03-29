from django.db import models
from django.utils.translation import gettext_lazy as _
from lfs.catalog.models import Product


class IsSample(models.Model):
    """
    Stores whether a product is a sample.
    """

    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="is_sample", on_delete=models.CASCADE)

    def __str__(self):
        return "{} / {}".format(self.product.id, self.product.get_name())


class ActivityState(models.Model):
    """
    Stores whether a variant has activated samples.
    """

    product = models.ForeignKey(
        Product, verbose_name=_("Product"), related_name="active_samples", on_delete=models.CASCADE
    )


class ProductSamplesRelation(models.Model):
    """
    Relates samples to products.
    """

    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="products", on_delete=models.CASCADE)
    sample = models.ForeignKey(Product, verbose_name=_("Sample"), related_name="samples", on_delete=models.CASCADE)

    def __str__(self):
        return "{} / {} <- {} / {}".format(
            self.product.id, self.product.get_name(), self.sample.id, self.sample.get_name()
        )
