# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import MapPageView

# This is a optional urls, for a basic site
# if you need some costuimizations, subclass all views
# and generata own urls.py

urlpatterns = patterns('',
    url(r"^$", MapPageView.as_view(), name="map-page"),
)
