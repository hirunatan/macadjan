from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from omap.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'', include('macadjan.urls', namespace='macadjan')),
    url(r'^admin/', include(admin.site.urls)),
)
