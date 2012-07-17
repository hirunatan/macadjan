# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import MapPageView

urlpatterns = patterns('',
    url(r"^$", MapPageView.as_view(), name="map-page"),
)
