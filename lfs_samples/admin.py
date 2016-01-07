# django imports
from django.contrib import admin

# lfs imports
from . models import IsSample
from . models import ProductSamplesRelation

admin.site.register(ProductSamplesRelation)
admin.site.register(IsSample)
