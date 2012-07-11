# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.conf import settings

from . import models

def current_site_info(request):
    '''Adds the site info for the current site to all template contexts.'''
    current_site = Site.objects.get_current()
    try:
        site_info = current_site.site_info
        return {'current_site_info': site_info}
    except models.SiteInfo.DoesNotExist:
        return {'current_site_info': None}

