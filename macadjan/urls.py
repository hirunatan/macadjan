# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import HomeView, MapPageView, MapIframeView

urlpatterns = patterns('',
    url(r"^$", HomeView.as_view(), name="home"),

    url(r'^map/(?P<category_slug>[a-zA-Z0-9_\-]+)/(?P<subcategory_slug>[a-zA-Z0-9_\-]+)/$',
        MapPageView.as_view(), name='map-page'),
    url(r'^map/(?P<category_slug>[a-zA-Z0-9_\-]+)/$',
        MapPageView.as_view(), name='map-page'),
    url(r'^map/$',
        MapPageView.as_view(), name='map-page'),

    url(r'^map_iframe/(?P<category_slug>[a-zA-Z0-9_\-]+)/(?P<subcategory_slug>[a-zA-Z0-9_\-]+)/$',
        MapIframeView.as_view(), name='map-iframe'),
    url(r'^map_iframe/(?P<category_slug>[a-zA-Z0-9_\-]+)/$',
        MapIframeView.as_view(), name='map-iframe'),
    url(r'^map_iframe/$',
        MapIframeView.as_view(), name='map-iframe'),

)

