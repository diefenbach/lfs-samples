import json

# django imports
from django.contrib.auth.decorators import permission_required
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# lfs.imports
from lfs.caching.utils import lfs_get_object_or_404
from lfs.catalog.models import Category
from lfs.catalog.models import Product
from lfs.catalog.settings import VARIANT
from lfs.core.utils import LazyEncoder

from . models import ActivityState
from . models import ProductSamplesRelation
from . utils import add_sample
from . utils import has_active_samples
from . utils import remove_sample


def get_parameter(r, p, default=None, with_session=True):
    if with_session:
        return r.GET.get(p, r.POST.get(p, r.session.get(p, default)))
    else:
        return r.GET.get(p, r.POST.get(p, default))


# Parts
@permission_required("core.manage_shop")
def manage_samples(request, product_id):
    product = Product.objects.get(pk=product_id)
    samples = ProductSamplesRelation.objects.filter(product_id=product_id)

    # amount options
    amount_options = []
    for value in (10, 25, 50, 100):
        amount_options.append({
            "value": value,
            "selected": value == request.session.get("samples-amount")
        })

    samples_inline = manage_samples_inline(request, product_id, as_string=True)

    result = render_to_string("lfs_samples/samples.html", RequestContext(request, {
        "product": product,
        "samples": samples,
        "amount_options": amount_options,
        "samples_inline": samples_inline,
        "has_active_samples": has_active_samples(product),
    }))

    return mark_safe(result)


@permission_required("core.manage_shop")
def manage_samples_inline(request, product_id, as_string=False, template_name="lfs_samples/samples_inline.html"):
    """View which shows all samples for the product with the passed id.
    """
    product = Product.objects.get(pk=product_id)

    samples = []
    samples_ids = []
    for psr in ProductSamplesRelation.objects.filter(product_id=product_id):
        samples.append(psr.sample)
        samples_ids.append(psr.sample.id)

    s = request.session

    page = get_parameter(request, "page", default=1)

    # If we get the parameter ``keep-filters`` or ``page`` we take the
    # filters out of the request resp. session. The request takes precedence.
    # The page parameter is given if the user clicks on the next/previous page
    # links. The ``keep-filters`` parameters is given is the users adds/removes
    # products. In this way we keeps the current filters when we needed to. If
    # the whole page is reloaded there is no ``keep-filters`` or ``page`` and
    # all filters are reset as they should.

    if get_parameter(request, "keep-filters", with_session=False) or page:
        filter_ = get_parameter(request, "filter")
        category_filter = get_parameter(request, "samples_category_filter")
    else:
        filter_ = get_parameter(request, "filter", with_session=False)
        category_filter = get_parameter(request, "samples_category_filter", with_session=False)

    # The current filters are saved in any case for later use.
    s["samples_page"] = page
    s["filter"] = filter_
    s["samples_category_filter"] = category_filter

    try:
        s["samples-amount"] = int(get_parameter(request, "samples-amount"))
    except TypeError:
        s["samples-amount"] = 25

    filters = Q()
    if filter_:
        filters &= (Q(name__icontains=filter_) | Q(sku__icontains=filter_))
        filters |= (Q(sub_type=VARIANT) & Q(active_sku=False) & Q(parent__sku__icontains=filter_))
        filters |= (Q(sub_type=VARIANT) & Q(active_name=False) & Q(parent__name__icontains=filter_))

    if category_filter:
        if category_filter == "None":
            filters &= Q(categories=None)
        elif category_filter == "All":
            pass
        else:
            # First we collect all sub categories and using the `in` operator
            category = lfs_get_object_or_404(Category, pk=category_filter)
            categories = [category]
            categories.extend(category.get_all_children())
            filters &= Q(categories__in=categories)

    products = Product.objects.filter(filters).exclude(pk__in=samples_ids).exclude(pk=product.pk)
    paginator = Paginator(products, s["samples-amount"])

    total = products.count()
    try:
        page = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        page = 0

    result = render_to_string(template_name, RequestContext(request, {
        "product": product,
        "samples": samples,
        "total": total,
        "page": page,
        "paginator": paginator,
        "filter": filter_,
    }))

    if as_string:
        return result
    else:
        return HttpResponse(
            json.dumps({
                "html": [["#samples-inline", result]],
            }), content_type='application/json')


# Actions
@permission_required("core.manage_shop")
def load_tab(request, product_id):
    """
    """
    samples = manage_samples(request, product_id)
    return HttpResponse(samples)


@permission_required("core.manage_shop")
def add_samples(request, product_id):
    """Adds passed samples (by request body) to product with passed id.
    """
    parent_product = Product.objects.get(pk=product_id)

    for temp_id in request.POST.keys():
        if temp_id.startswith("product") is False:
            continue

        temp_id = temp_id.split("-")[1]
        add_sample(parent_product, temp_id)

        # This isn't necessary but it cleans the cache. See lfs.cache listeners
        # for more
        parent_product.save()

    html = [["#samples-inline", manage_samples_inline(request, product_id, as_string=True)]]

    result = json.dumps({
        "html": html,
        "message": _(u"Samples have been added.")
    }, cls=LazyEncoder)

    return HttpResponse(result, content_type='application/json')


@permission_required("core.manage_shop")
def remove_samples(request, product_id):
    """Removes passed samples from product with passed id.
    """
    parent_product = Product.objects.get(pk=product_id)

    for temp_id in request.POST.keys():
        if temp_id.startswith("product") is False:
            continue

        temp_id = temp_id.split("-")[1]
        remove_sample(product=parent_product, sample_id=temp_id)

        # This isn't necessary but it cleans the cache. See lfs.cache listeners
        # for more
        parent_product.save()

    html = [["#samples-inline", manage_samples_inline(request, product_id, as_string=True)]]

    result = json.dumps({
        "html": html,
        "message": _(u"Samples have been removed.")
    }, cls=LazyEncoder)

    return HttpResponse(result, content_type='application/json')


@permission_required("core.manage_shop")
def update_samples_state(request, product_id):
    """Updates samples activity state for variants.
    """
    product = Product.objects.get(pk=product_id)
    if request.POST.get("samples_activity_state"):
        ActivityState.objects.get_or_create(product=product)
    else:
        try:
            activity_state = ActivityState.objects.get(product=product)
        except ActivityState.DoesNotExist:
            pass
        else:
            activity_state.delete()

    product.save()

    html = [["#samples-inline", manage_samples_inline(request, product_id, as_string=True)]]

    result = json.dumps({
        "html": html,
        "message": _(u"Samples have been updated.")
    }, cls=LazyEncoder)

    return HttpResponse(result, content_type='application/json')
