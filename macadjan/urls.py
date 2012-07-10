# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import MainPageView

# This is a optional urls, for a basic site
# if you need some costuimizations, subclass all views
# and generata own urls.py

urlpatterns = patterns('',
    url(r"^$", MainPageView.as_view(), name="map-main"),
)
