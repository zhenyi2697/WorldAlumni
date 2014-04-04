from django.conf.urls import patterns, include, url

import backend
from backend.models import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'backend.views.home', name='static_home'),
    #url(r'^loggedin/', 'backend.views.loggedin', name='loggedin'),
    # url(r'^WorldAlumni/', include('WorldAlumni.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    
    url('', include('social.apps.django_app.urls', namespace='social'))
)
