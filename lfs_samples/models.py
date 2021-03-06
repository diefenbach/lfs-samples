from django.db import models
from django.utils.translation import ugettext_lazy as _
from lfs.catalog.models import Product


class IsSample(models.Model):
    """
    Stores whether a product is a sample.
    """
    product = models.ForeignKey(Product, verbose_name=_(u"Product"), related_name="is_sample")

    def __unicode__(self):
        return u"{} / {}".format(self.product.id, self.product.get_name())


class ActivityState(models.Model):
    """
    Stores whether a variant has activated samples.
    """
    product = models.ForeignKey(Product, verbose_name=_(u"Product"), related_name="active_samples")


class ProductSamplesRelation(models.Model):
    """
    Relates samples to products.
    """
    product = models.ForeignKey(Product, verbose_name=_(u"Product"), related_name="products")
    sample = models.ForeignKey(Product, verbose_name=_(u"Sample"), related_name="samples")

    def __unicode__(self):
        return u"{} / {} <- {} / {}".format(self.product.id, self.product.get_name(), self.sample.id, self.sample.get_name())
