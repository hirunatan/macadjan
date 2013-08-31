# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

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
#    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'marker_url', 'is_active') # Fields shown in the entity list
    list_filter = ('is_active',)         # Fields you can filter by in the entity list
    prepopulated_fields = {'slug': ('name',)}
    actions = [make_active, make_inactive]
#    inlines = [
#        SubCategoryInline,
#    ]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'slug', 'marker_url', 'is_active') # Fields shown in the entity list
    list_filter = ('is_active', 'category',)         # Fields you can filter by in the entity list
    prepopulated_fields = {'slug': ('name',)}
    actions = [make_active, make_inactive]


class TagCollectionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',) # Fields shown in the entity list
    prepopulated_fields = {'slug': ('name',)}


class EntityTagAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',) # Fields shown in the entity list
    list_filter = ('collection',)          # Fields you can filter by in the entity list
    prepopulated_fields = {'slug': ('name',)}


class MapSourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


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
        ('Visibilidad de campos del formulario de solicitud', {
            'classes': ('collapse',),
            'fields': ('proponent_email_field_enabled','proponent_comment_field_enabled','alias_field_enabled',
            'summary_field_enabled','subcategories_field_enabled','address_1_field_enabled',
            'address_2_field_enabled','zipcode_field_enabled','city_field_enabled','province_field_enabled',
            'country_field_enabled','zone_field_enabled','latitude_field_enabled','longitude_field_enabled',
            'contact_phone_1_field_enabled','contact_phone_2_field_enabled','fax_field_enabled','email_field_enabled',
            'email_2_field_enabled','web_field_enabled','web_2_field_enabled','contact_person_field_enabled',
            'creation_year_field_enabled','legal_form_field_enabled','description_field_enabled','goals_field_enabled',
            'finances_field_enabled','social_values_field_enabled','how_to_access_field_enabled',
            'networks_member_field_enabled','networks_works_with_field_enabled','ongoing_projects_field_enabled',
            'needs_field_enabled','offerings_field_enabled','additional_info_field_enabled')

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
admin.site.register(MapSource, MapSourceAdmin)


# ModelAdmin for users. If your app needs to override ModelAdmin for users, you'll need to
# subclass this or to add a similar Inline.

class MacadjanUserProfileInline(admin.StackedInline):
    model = MacadjanUserProfile
    can_delete = False
    verbose_name_plural = _(u'perfil Macadjan')

class MacadjanUserAdmin(UserAdmin):
    inlines = (MacadjanUserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, MacadjanUserAdmin)


# ModelAdmin for entities. This is an abstract class. You must write a derived
# one and register your Entity subclass with it.

class EntityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'alias', 'main_subcategory', 'modification_date', 'is_active') # Fields shown in the entity list
    filter_vertical = ('subcategories', 'tags',)  # Fields that use a selection widget instead a multi select
    list_filter = ('is_active', 'subcategories',) # Fields you can filter by in the entity list
    search_fields = ('name', 'alias',) # Fields searched by the input bux in the entity list
    prepopulated_fields = {'slug': ('name',)}
    actions = [make_active, make_inactive, 'geolocalize']

    def geolocalize(self, request, queryset):
        #for obj in queryset:
        #    task__geolocalize_entity.delay(obj.pk)
        self.message_user(request, _(u'Se han lanzado %(num)d geolocalizaciones') % {'num': queryset.count()})

    geolocalize.short_description = _(u'Geolocalizar todos los seleccionados')


    # TODO: it would be good to have also categories in list_filter, but currently the admin only supports
    # real fields, not properties or methods or fields in other tables. We could add a 'category' field to
    # Entity class, and sincronize it with signals. To think later...


    # Restrictions for users with map source. Ideas taken from
    # http://www.alextreme.org/misc/sub_admin.py

    def _auto_hide_map_source(self, request):
        '''
        Map source users can not see map_source fields.
        '''
        user = request.user
        profile = MacadjanUserProfile.objects.get_for_user(user)
        if not user.is_superuser and profile and profile.map_source:
            self.exclude = ['map_source']
        else:
            self.exclude = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        Admin users that have a profile with a not null map_source, get it as a
        default value when creating entities, although they can change it later.
        '''
        formfield = super(EntityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        user = request.user
        profile = MacadjanUserProfile.objects.get_for_user(user)
        if db_field.name != 'map_source' or not user.is_superuser \
           or not profile or not profile.map_source:
            return formfield

        kwargs['initial'] = profile.map_source
        return db_field.formfield(**kwargs)

    def add_view(self, request, form_url='', extra_context = None):
        '''
        Hide map_source in the add page in the admin.
        '''
        self._auto_hide_map_source(request)
        return super(EntityAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context = None):
        '''
        Hide map_source in the change page in the admin.
        '''
        self._auto_hide_map_source(request)
        return super(EntityAdmin, self).change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_content = None):
        '''
        Hide map source filter in the change list page in the admin.
        '''
        user = request.user
        profile = MacadjanUserProfile.objects.get_for_user(user)
        self.list_filter = tuple(set(self.list_filter) - set(('map_source',)))
        if user.is_superuser or not profile or not profile.map_source:
            self.list_filter = self.list_filter + (('map_source',))
        return super(EntityAdmin, self).changelist_view(request, extra_content)

    def history_view(self, request, object_id, extra_context = None):
        '''
        Although we wouldn't have permission to view this object, the history view
        for an object does show the name of the object anyway.
        '''
        user = request.user
        profile = MacadjanUserProfile.objects.get_for_user(user)
        if not user.is_superuser and profile and profile.map_source:
            obj = get_object_or_404(self.model, pk = object_id)
            if obj.map_source != profile.map_source:
                raise Http404('No %s matches the given query.' % self.model._meta.object_name)
        return super(EntityAdmin, self).history_view(request, object_id, extra_context = None)

    def save_model(self, request, obj, form, change):
        '''
        When the user hits Save on an add/modify admin page, automatically set map_source.
        '''
        user = request.user
        profile = MacadjanUserProfile.objects.get_for_user(user)
        if not user.is_superuser and profile and profile.map_source:
            if change and obj.map_source != profile.map_source:
                raise Http404('No such object')
            else:
                obj.map_source = profile.map_source
        obj.save()

    def queryset(self, request):
        '''
        Called when the user hits the overview page.
        Limit the objects shown in the main list to only ones from user map source.
        '''
        user = request.user
        profile = MacadjanUserProfile.objects.get_for_user(user)
        if not user.is_superuser and profile and profile.map_source:
            queryset = self.model.objects.filter(map_source = profile.map_source)
        else:
            queryset = self.model.objects.all()
        return queryset

    def has_change_permission(self, request, obj = None):
        '''
        Called in various places in contrib.admin to determine if the user has permission to change this object.
        The user has no permission if the map_source is different.
        '''
        has_class_permission = super(EntityAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None:
            user = request.user
            profile = MacadjanUserProfile.objects.get_for_user(user)
            if not user.is_superuser and profile and profile.map_source:
                if obj.map_source != profile.map_source:
                    return False
        return True
