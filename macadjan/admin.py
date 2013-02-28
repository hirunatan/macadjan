# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.contrib import admin

from .models import *
#from .async_tasks import *

# Generic actions to activate and desactivate models.
# Can be attached as actions to different ModelAdmins.

def make_active(modeladmin, request, queryset):
    rows_updated = queryset.update(is_active = True)
    modeladmin.message_user(request, _(u'Se han activado %(num)d elementos') % {'num': rows_updated})

make_active.short_description = _(u'Activar todos los seleccionados')

def make_inactive(modeladmin, request, queryset):
    rows_updated = queryset.update(is_active = False)
    modeladmin.message_user(request, _(u'Se han desactivado %(num)d elementos') % {'num': rows_updated})

make_inactive.short_description = _(u'Desactivar todos los seleccionados')


# ModelAdmins for macadjan models.

# TODO: test if it's better to have subcategories inlined or not
#class SubCategoryInline(admin.StackedInline):
#    model = SubCategory
#    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'marker_url', 'is_active') # Fields shown in the entity list
    list_filter = ('is_active',)         # Fields you can filter by in the entity list
    prepopulated_fields = {"slug": ("name",)}
    actions = [make_active, make_inactive]
#    inlines = [
#        SubCategoryInline,
#    ]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'slug', 'marker_url', 'is_active') # Fields shown in the entity list
    list_filter = ('is_active', 'category',)         # Fields you can filter by in the entity list
    prepopulated_fields = {"slug": ("name",)}
    actions = [make_active, make_inactive]


class TagCollectionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',) # Fields shown in the entity list
    prepopulated_fields = {"slug": ("name",)}


class EntityTagAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',) # Fields shown in the entity list
    list_filter = ('collection',)          # Fields you can filter by in the entity list
    prepopulated_fields = {"slug": ("name",)}

class SiteInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Configuración del sitio', {
            'classes': ('collapse',),
            'fields': ('site', 'website_name', 'website_subtitle', 'website_description','footer_line')
        }),
        ('Configuración del mapa', {
            'classes': ('collapse',),
            'fields': ('map_bounds_left', 'map_bounds_right', 'map_bounds_bottom','map_bounds_top',
            'map_zoom_levels', 'map_max_resolution','map_units','map_initial_lon','map_initial_lat',
            'map_initial_zoom')
        }),
        ('Formulario de solicitud', {
            'classes': ('collapse',),
            'fields': ('new_entity_proposal_enabled','entity_change_proposal_enabled','new_entity_proposal_title',
            'new_entity_proposal_text','change_proposal_title','change_proposal_text','proposal_bottom_text')
        }),
        ('Textos de ayuda', {
            'classes': ('collapse',),
            'fields': ('description_hints','goals_hints','finances_hints','social_values_hints',
                       'how_to_access_hints','networks_member_hints','networks_works_with_hints',
                       'ongoing_projects_hints','needs_hints','offerings_hints','additional_info_hints')
        }),
    )

admin.site.register(SiteInfo, SiteInfoAdmin)
admin.site.register(EntityType)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(TagCollection, TagCollectionAdmin)
admin.site.register(EntityTag, EntityTagAdmin)


# ModelAdmin for entities. This is an abstract class. You must write a derived
# one and register your Entity subclass with it.

class EntityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'alias', 'main_subcategory', 'modification_date', 'is_active') # Fields shown in the entity list
    filter_vertical = ('subcategories', 'tags',)   # Fields that use a selection widget instead a multi select
    list_filter = ('is_active', 'subcategories',)         # Fields you can filter by in the entity list
    search_fields = ('name', 'alias',)       # Fields searched by the input bux in the entity list
    prepopulated_fields = {"slug": ("name",)}
    actions = [make_active, make_inactive, 'geolocalize']

    def geolocalize(self, request, queryset):
        #for obj in queryset:
        #    task__geolocalize_entity.delay(obj.pk)
        self.message_user(request, _(u'Se han lanzado %(num)d geolocalizaciones') % {'num': queryset.count()})

    geolocalize.short_description = _(u'Geolocalizar todos los seleccionados')


    # TODO: it would be good to have also categories in list_filter, but currently the admin only supports
    # real fields, not properties or methods or fields in other tables. We could add a "category" field to
    # Entity class, and sincronize it with signals. To think later...

