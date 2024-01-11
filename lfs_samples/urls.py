from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^samples-tab/(?P<product_id>\d*)$", views.load_tab, name="lfs_manage_samples_tab"),
    re_path(r"^samples/(?P<product_id>\d*)$", views.manage_samples, name="lfs_manage_samples"),
    re_path(r"^samples-inline/(?P<product_id>\d*)$", views.manage_samples_inline, name="lfs_manage_samples_inline"),
    re_path(r"^add-samples/(?P<product_id>\d*)$", views.add_samples, name="lfs_manage_add_samples"),
    re_path(r"^remove-samples/(?P<product_id>\d*)$", views.remove_samples, name="lfs_manage_remove_samples"),
    re_path(
        r"^update-samples-state/(?P<product_id>\d*)$",
        views.update_samples_state,
        name="lfs_manage_update_samples_state",
    ),
    re_path(r"^update-is-samples/(?P<product_id>\d*)$", views.update_is_sample, name="lfs_manage_update_is_sample"),
]
