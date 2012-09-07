# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import MapPageView, MapIframeView

urlpatterns = patterns('',
    url(r"^$", MapPageView.as_view(), name="map-page"),
    url(r"^iframe/$", MapIframeView.as_view(), name="map-iframe"),
)

