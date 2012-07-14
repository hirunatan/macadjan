# -*- coding: utf-8 -*-

from django.contrib import admin

from macadjan.admin import EntityAdmin

from . import models

admin.site.register(models.SampleEntity, EntityAdmin)

