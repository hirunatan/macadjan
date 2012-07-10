# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models

admin.site.register(models.EntityType)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.TagCollection)
admin.site.register(models.EntityTag)
