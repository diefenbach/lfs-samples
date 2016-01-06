from . models import ProductSamplesRelation
from . models import ActivityState


def get_samples(product):
    samples = []
    if product.is_variant() and has_active_samples(product) is False:
        product = product.parent

    for product_samples_relation in ProductSamplesRelation.objects.filter(product=product):
        samples.append(product_samples_relation.sample)
    return samples


def has_samples(product):
    return ProductSamplesRelation.objects.filter(product=product).exists()


def add_sample(product, sample_id):
    ProductSamplesRelation.objects.create(product=product, sample_id=sample_id)


def remove_sample(product, sample_id):
    ProductSamplesRelation.objects.filter(product=product, sample_id=sample_id).delete()


def has_active_samples(product_or_id):
    try:
        if isinstance(product_or_id, int):
            ActivityState.objects.get(product_id=product_or_id)
        else:
            ActivityState.objects.get(product=product_or_id)
    except ActivityState.DoesNotExist:
        return False
    else:
        return True
