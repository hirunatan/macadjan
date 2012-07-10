# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models


class SubCategoryInline(admin.StackedInline):
    model = models.SubCategory
    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryInline,
    ]

admin.site.register(models.EntityType)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SubCategory)
admin.site.register(models.TagCollection)
admin.site.register(models.EntityTag)
