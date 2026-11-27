# lfs-samples

Product samples for [django-lfs](https://pypi.org/project/django-lfs/) (LFS).

A shop manager marks products as samples and assigns them to other products. A customer can then order the sample
of a product from its product page.

## What it does

- Adds a **Samples** tab to every product in the LFS management interface.
- Stores in its own tables:
  - whether a product *is a sample*,
  - which samples belong to a product,
  - for variants: whether the variant has *its own samples* or uses those of its parent product.
- Provides template tags to show a product's samples in the shop.

A sample is an ordinary LFS product. When a customer orders it, it goes into the cart like any other product, with
its own price, stock and delivery settings. To give samples away for free, give the sample products a price of 0.

## Requirements

- django-lfs >= 1.0, < 2 (which requires Django >= 5.2, < 6)
- Python >= 3.12

## Installation

1. Install the package:

   ```sh
   pip install lfs-samples
   ```

2. Add it to `INSTALLED_APPS`, after the LFS apps:

   ```python
   INSTALLED_APPS = [
       # ... the LFS apps ...
       "lfs_samples",
   ]
   ```

3. Include its URLs in your project's `urls.py`. **This step is required:** the app registers the Samples tab as
   soon as it is installed, and without these URLs every product page in the management interface fails with
   `NoReverseMatch` for `lfs_manage_product_samples`.

   ```python
   from django.urls import include, path

   urlpatterns = [
       # ...
       path("manage/", include("lfs.manage.urls")),
       path("manage/samples/", include("lfs_samples.urls")),
   ]
   ```

   The templates build all links with `{% url %}`, so any prefix works. `manage/samples/` is recommended: all
   views of the app belong to the management interface (they require the `core.manage_shop` permission), so they
   share its `manage/` prefix.

4. Create the tables:

   ```sh
   python manage.py migrate lfs_samples
   ```

## Usage in the management interface

Open a product in the management interface and select the **Samples** tab.

- **Is sample**: marks the product as a sample. Only products marked this way can be assigned to other products.
  A sample has no samples of its own, so the rest of the tab is hidden for it.
- **Active samples** (variants only): when checked, the variant uses the samples assigned to it. When unchecked,
  the variant uses the samples of its parent product.
- **Selectable Samples / Selected Samples**: the left list shows the products marked as samples that are not yet
  assigned (searchable by name or SKU, filterable by category); select some and add them to the product. The right
  list shows the samples assigned to the product; select some and remove them.

## Showing samples in the shop

Load the template tags with `{% load lfs_samples_tags %}`. They read `product` from the template context:

- `{% product_samples %}` sets `product_samples` to the list of the product's samples. For a variant without
  active samples it returns the samples of the parent product.
- `{% is_sample %}` sets `is_sample` to whether the product is a sample.
- `{% ifproducthassamples %} ... {% else %} ... {% endifproducthassamples %}` renders its first part when samples
  are assigned to the product itself (it does not fall back to the parent product).

LFS's product form accepts a sample directly: submitted with `action=add-sample-to-cart` and the sample's id as
`sample_id`, it adds the sample to the cart. Inside the product form, for example:

```django
{% load i18n lfs_samples_tags %}
{% product_samples %}
{% with sample=product_samples.0 %}
    {% if sample %}
        <input type="hidden" name="sample_id" value="{{ sample.id }}">
        <button type="submit" name="action" value="add-sample-to-cart">{% trans "Order a free sample" %}</button>
    {% endif %}
{% endwith %}
```

lfs-theme already shows this button on the product page when `lfs_samples` is installed.

The app comes with a German translation.

## Development

The tests use pytest with pytest-django and an in-memory SQLite database (see `pytest.ini` and
`lfs_samples/tests/settings.py`). In an environment with django-lfs, pytest and pytest-django installed:

```sh
pip install -e .
python -m pytest
```

## License

BSD 3-Clause License, see `LICENSE.txt`.
