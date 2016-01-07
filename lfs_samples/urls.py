from django.conf.urls import patterns, url

urlpatterns = patterns('lfs_samples.views',
    url(r'^samples-tab/(?P<product_id>\d*)$', "load_tab", name="lfs_manage_samples_tab"),
    url(r'^samples/(?P<product_id>\d*)$', "manage_samples", name="lfs_manage_samples"),
    url(r'^samples-inline/(?P<product_id>\d*)$', "manage_samples_inline", name="lfs_manage_samples_inline"),
    url(r'^add-samples/(?P<product_id>\d*)$', "add_samples", name="lfs_manage_add_samples"),
    url(r'^remove-samples/(?P<product_id>\d*)$', "remove_samples", name="lfs_manage_remove_samples"),
    url(r'^update-samples-state/(?P<product_id>\d*)$', "update_samples_state", name="lfs_manage_update_samples_state"),
    url(r'^update-is-samples/(?P<product_id>\d*)$', "update_is_sample", name="lfs_manage_update_is_sample"),
)
