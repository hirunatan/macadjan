# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import RedirectView
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext as _

from superview.views import SuperView as View

from .models import Category, SubCategory
from .utils import to_json
from .forms import MapArgumentsForm, ListArgumentsForm


class HomeView(RedirectView):
    '''Site root -> redirect to map view'''
    def get_redirect_url(self, **kwargs):
        return reverse('map-page')


class CategoriesView(View):

    def get(self, request):
        categories = [
            category.to_dict(include_subcategories = True) for category in Category.objects.actives_only()
        ]
        return HttpResponse(to_json(categories), content_type='application/json')


class CategoryResponseMixin(object):
    def get_categories_query_set(self):
        return Category.objects.actives_only()

    def categories_as_json(self):
        """
        Get categories list on json format.
        """
        return to_json([obj.to_dict() for obj in self.get_categories_query_set()])


class SubCategoriesResponseMixin(object):
    def get_subcategories_query_set(self):
        return SubCategory.objects.actives_only()

    def subcategories_as_json(self):
        """
        Get subcategory list on json format.
        """
        return to_json([obj.to_dict() for obj in self.get_subcategories_query_set()])


class MapView(CategoryResponseMixin, SubCategoriesResponseMixin, View):
    '''
    Base class for a view that shows a map page, thay may have the map itself,
    a filter frame and a list frame, all of them synchronized.

    It can receive optional filtering and zooming parameters.
    '''
    template_name = None

    def get(self, request, category_slug = None, subcategory_slug = None):
        if not self.template_name:
            raise ImproperlyConfigured(_(u'You must subclass MapView and define template_name.'))
        context = self.get_context_data(request, category_slug, subcategory_slug)
        return self.render_to_response(self.template_name, context)

    def get_context_data(self, request, category_slug, subcategory_slug):
        map_arguments = self.get_map_arguments(request, category_slug, subcategory_slug)
        context = {
            'map_arguments': map_arguments,
        }
        return context

    def get_map_arguments(self, request, category_slug, subcategory_slug):
        return MapArguments(request, category_slug, subcategory_slug)


class MapArguments(object):
    '''
    The set of arguments accepted by the map view.

    Some of the arguments are received in the url, and the other ones come in GET data. For some of
    them, if not given, default values are taken from SiteInfo.

    The args in the url are:
      - category_slug: slug of the category to filter
      - subcategory_slug: slug of the subcategory to filter

    The args in GET are:
      - kw: url-quoted, space-separated list of keywords to filter
      - lon: longitude of the initial center (default: site_info.map_initial_lon)
      - lat: latitude of the initial center (default: site_info.map_initial_lat)
      - z: initial zoom level (default: site_info.map_initial_zoom)
      - bl: left coordinate of the map outer bounds (default: site_info.map_bounds_left)
      - br: right coordinate of the map outer bounds (default: site_info.map_bounds_right)
      - bt: top coordinate of the map outer bounds (default: site_info.map_bounds_top)
      - bb: bottom coordinate of the map outer bounds (default: site_info.map_bounds_bottom)
    '''
    def __init__(self, request, category_slug, subcategory_slug):
        self.filter_category = get_object_or_404(Category, slug = category_slug) if category_slug else None
        self.filter_subcategory = get_object_or_404(SubCategory, slug = subcategory_slug) if subcategory_slug else None
        self.filter_keywords = ''
        self.initial_lon = 0
        self.initial_lat = 0
        self.initial_zoom = 0
        self.bounds_left = 0
        self.bounds_right = 0
        self.bounds_top = 0
        self.bounds_bottom = 0

        arguments_form = MapArgumentsForm(request.GET)
        if arguments_form.is_valid():
            self.filter_keywords = arguments_form.cleaned_data['kw']
            self.initial_lon = arguments_form.cleaned_data['lon']
            self.initial_lat = arguments_form.cleaned_data['lat']
            self.initial_zoom = arguments_form.cleaned_data['z']
            self.bounds_left = arguments_form.cleaned_data['bl']
            self.bounds_right = arguments_form.cleaned_data['br']
            self.bounds_top = arguments_form.cleaned_data['bt']
            self.bounds_bottom = arguments_form.cleaned_data['bb']

        site_info = None
        if not self.initial_lon or not self.initial_lat:
            if not site_info: site_info = Site.objects.get_current().site_info
            self.initial_lon = site_info.map_initial_lon
            self.initial_lat = site_info.map_initial_lat
        if not self.initial_zoom:
            if not site_info: site_info = Site.objects.get_current().site_info
            self.initial_zoom = site_info.map_initial_zoom
        if not self.bounds_left or not self.bounds_right or \
           not self.bounds_top or not self.bounds_bottom:
            if not site_info: site_info = Site.objects.get_current().site_info
            self.bounds_left = site_info.map_bounds_left
            self.bounds_right = site_info.map_bounds_right
            self.bounds_top = site_info.map_bounds_top
            self.bounds_bottom = site_info.map_bounds_bottom


class MapPageView(MapView):
    template_name = "macadjan/map-page.html"


class MapIframeView(MapView):
    template_name = "macadjan/map-iframe.html"


class Entities(View):
    '''
    Base class with a view that gets the list of entities, filtered by categories and bounds.
    The format of the returned list is configured in subclasses.
    '''

    model = None

    def find_entities(self, request, *args, **kwargs):
        if not self.model:
            raise ImproperlyConfigured(_(u'You must subclass Entities view and define the model.'))

        filter_arguments = ListArgumentsForm(request.GET)
        if not filter_arguments.is_valid():
            return self.model.objects_active.none()

        if filter_arguments.cleaned_data['left'] and filter_arguments.cleaned_data['right'] and \
           filter_arguments.cleaned_data['top'] and filter_arguments.cleaned_data['bottom']:

            entities = self.model.objects_active.entities_in_area(
                filter_arguments.cleaned_data['left'],
                filter_arguments.cleaned_data['right'],
                filter_arguments.cleaned_data['top'],
                filter_arguments.cleaned_data['bottom']
            )

        else:
            entities = self.model.objects_active.all()

        entities = self.model.objects_active.filter_by_cat(
            entities,
            filter_arguments.cleaned_data['cat'],
            filter_arguments.cleaned_data['subcat'],
        )
        entities_list = self.model.objects_active.filter_with_keywords(
           entities,
           filter_arguments.cleaned_data['kw'],
        )

        return entities_list


class EntitiesText(Entities):
    '''Get entities in a format readable by the openlayers scripts.'''

    def get(self, request, *args, **kwargs):
        entities_list = self.find_entities(request, *args, **kwargs)

        text = u'lat\tlon\ticon\ticonSize\ticonOffset\ttitle\tdescription\tpopupSize\n'

        for entity in entities_list:
            if entity.latitude and entity.longitude:
                title, description = (
                    u'<a href="%s" target="_blank">%s</a>' % ('http://' + Site.objects.get_current().domain +
                                                        reverse('entity', kwargs={'entity_slug': entity.slug}),
                                                        entity.name),
                    u'<br/>%s' % entity.summary
                    )

                text += u'%f\t%f\t%s\t%d,%d\t%d,%d\t%s\t%s\t%d,%d\n' % (entity.latitude,
                                        entity.longitude, settings.STATIC_URL + entity.marker_url,
                                        32, 32, -16, -16, title, description, 300, 120)

        return HttpResponse(text, content_type='text/plain')


class EntitiesList(Entities):
    '''Get entities list formatted for display.'''

    template_name = "macadjan/list-block.html"

    def get(self, request, *args, **kwargs):
        entities_list = self.find_entities(request, *args, **kwargs)
        context = {
            "entities_list": entities_list
        }
        return self.render_to_response(self.template_name, context)


class EntitiesKml(Entities):
    '''Get entities list as a KML file.'''

    template_name = "macadjan/list-kml.kml"

    def get(self, request, *args, **kwargs):
        entities_list = self.find_entities(request, *args, **kwargs)
        entities_list = entities_list.order_by('-modification_date')
        entities_urls = [(entity, 'http://' + Site.objects.get_current().domain +
                                  reverse('entity', kwargs={'entity_slug': entity.slug}))
                         for entity in entities_list]
        context = {
            "entities_urls": entities_urls
        }
        return self.render_to_response(self.template_name, context,
                    mimetype = 'application/vnd.google-earth.kml+xml')


class EntitiesGeoRSS(Entities):
    '''Get entities list as a GeoRSS file.'''

    template_name = "macadjan/list-georss.xml"

    def get(self, request, *args, **kwargs):
        entities_list = self.find_entities(request, *args, **kwargs)
        entities_list = entities_list.order_by('-modification_date')
        entities_urls = [(entity, 'http://' + Site.objects.get_current().domain +
                                  reverse('entity', kwargs={'entity_slug': entity.slug}))
                         for entity in entities_list]
        context = {
            "entities_urls": entities_urls
        }
        return self.render_to_response(self.template_name, context,
            mimetype = 'application/rss+xml')


class Entity(View):
    '''
    Base class with a view that display the complete card of one entity.
    '''

    model = None
    template_name = "macadjan/entity-page.html"

    def get(self, request, entity_slug, *args, **kwargs):
        if not self.model:
            raise ImproperlyConfigured()

        entity = get_object_or_404(self.model, slug = entity_slug)
        context = {
            'entity': entity
        }
        return self.render_to_response(self.template_name, context)

