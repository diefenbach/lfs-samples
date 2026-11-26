"""App configuration: registers the samples tab on the product management page."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LfsSamplesConfig(AppConfig):
    """Adds the "Samples" tab to every product."""

    name = "lfs_samples"
    verbose_name = _("Samples")

    def ready(self) -> None:
        """Register the product tab."""
        from lfs.manage.products.tabs import ProductTab, register_product_tab

        register_product_tab(
            ProductTab(
                key="samples",
                label=_("Samples"),
                url_name="lfs_manage_product_samples",
                template="manage/products/tabs/_samples.html",
            )
        )
