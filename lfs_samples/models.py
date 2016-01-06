from django.db import models
from django.utils.translation import ugettext_lazy as _
from lfs.catalog.models import Product


class ActivityState(models.Model):
    """
    Stores wether a variant has activated samples.
    """
    product = models.ForeignKey(Product, verbose_name=_(u"Product"), related_name="active_samples")


class ProductSamplesRelation(models.Model):
    """
    Relates samples to products.
    """
    product = models.ForeignKey(Product, verbose_name=_(u"Product"), related_name="products")
    sample = models.ForeignKey(Product, verbose_name=_(u"Sample"), related_name="samples")
