from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
                url(r'^api/check_binding/$', 'check_binding'),
                url(r'^api/nearby_users/$', 'nearby_users'),
                # url(r'^api/bindings/$', 'binding_list'),
                # url(r'^api/bindings/(?P<pk>[0-9]+)/$', 'binding_detail'),
            )
