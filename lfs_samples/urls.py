from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^samples-tab/(?P<product_id>\d*)$', views.load_tab, name="lfs_manage_samples_tab"),
    url(r'^samples/(?P<product_id>\d*)$', views.manage_samples, name="lfs_manage_samples"),
    url(r'^samples-inline/(?P<product_id>\d*)$', views.manage_samples_inline, name="lfs_manage_samples_inline"),
    url(r'^add-samples/(?P<product_id>\d*)$', views.add_samples, name="lfs_manage_add_samples"),
    url(r'^remove-samples/(?P<product_id>\d*)$', views.remove_samples, name="lfs_manage_remove_samples"),
    url(r'^update-samples-state/(?P<product_id>\d*)$', views.update_samples_state, name="lfs_manage_update_samples_state"),
    url(r'^update-is-samples/(?P<product_id>\d*)$', views.update_is_sample, name="lfs_manage_update_is_sample"),
]
