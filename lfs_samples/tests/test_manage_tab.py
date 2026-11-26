"""The add-on registers its "Samples" tab on the product management page (django-lfs no longer lists it itself)."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from lfs.catalog.models import Product


@pytest.fixture
def admin_client(client, db):
    call_command("lfs_init")
    client.force_login(get_user_model().objects.create_superuser("admin", "admin@example.com", "x"))
    return client


def test_samples_tab_is_listed_and_shows_its_content(admin_client):
    product = Product.objects.create(name="Board", slug="board", sku="B1", price=10, active=True)
    samples_url = reverse("lfs_manage_product_samples", args=[product.pk])

    data_page = admin_client.get(reverse("lfs_manage_product_data", args=[product.pk])).content.decode()
    samples_page = admin_client.get(samples_url).content.decode()

    assert samples_url in data_page
    assert 'id="samples-content"' in samples_page
