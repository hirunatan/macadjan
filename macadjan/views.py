# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from superview.views import SuperView as View
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext as _

from .models import Category, SubCategory
from .utils import to_json
from .forms import OpenLayersTileArgumentsForm,  ParamsValidationForm

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


class MapPageView(CategoryResponseMixin, SubCategoriesResponseMixin, View):
    template_name = "macadjan/map-page.html"

    def get(self, request):
        context = {
            "initial": self.initial_context_from_params()
        }
        return self.render_to_response(self.template_name, context)

    def initial_context_from_params(self):
        """
        Filter initial params from GET querystring.
        """
        initial_context = {}

        form = ParamsValidationForm(self.request.GET)
        if not form.is_valid():
            return initial_context

        initial_context.update(form.cleaned_data)

        if not initial_context.get('lat', '') or \
           not initial_context.get('lon', '') or \
           not initial_context.get('zoom', ''):

           site_info = Site.objects.get_current().site_info
           initial_context['lon'] = site_info.map_initial_lon
           initial_context['lat'] = site_info.map_initial_lat
           initial_context['zoom'] = site_info.map_initial_zoom

        return initial_context


class Entities(View):
    '''
    Base class with a view that gets the list of entities, filtered by categories and bounds.
    The format of the returned list is configured in subclasses.
    '''

    model = None

    def find_entities(self, request, *args, **kwargs):
        if not self.model:
            raise ImproperlyConfigured()

        filter_arguments = OpenLayersTileArguments(request)
        if not filter_arguments.is_valid:
            return []

        if filter_arguments.left and filter_arguments.right and \
                        filter_arguments.top and filter_arguments.bottom:
            entities = self.model.objects_active.entities_in_area(
                            filter_arguments.left,
                            filter_arguments.right,
                            filter_arguments.top,
                            filter_arguments.bottom,
                            filter_arguments.category,
                            filter_arguments.subcategory,
                            filter_arguments.map_source)
        else:
            entities = self.model.objects_active.all()
            entities = self.model.objects_active._entities_filter(
                            entities,
                            filter_arguments.category,
                            filter_arguments.subcategory,
                            filter_arguments.map_source)
        entities_list = self.model.objects_active.filter_with_keywords(
                               entities,
                               filter_arguments.keywords)

        return entities_list


class EntitiesText(Entities):
    '''Get entities in a format readable by the openlayers scripts.'''

    def get(self, request, *args, **kwargs):
        entities_list = self.find_entities(request, *args, **kwargs)

        text = u'lat\tlon\ticon\ticonSize\ticonOffset\ttitle\tdescription\tpopupSize\n'

        for entity in entities_list:
            title, description = (
                u'<a href="%s" target="_blank">%s</a>' % ('http://' + Site.objects.get_current().domain +
                                                              reverse('entity', kwargs={'entity_slug': entity.slug}),
                                                          entity.name),
                u'<br/>%s' % entity.summary
            )

            text += u'%f\t%f\t%s\t%d,%d\t%d,%d\t%s\t%s\t%d,%d\n' % (entity.latitude,
                            entity.longitude, settings.STATIC_URL + entity.marker_url,
                            32, 37, 0, -37, title, description, 300, 120)

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


class OpenLayersFeatures(object):
    '''
    A number of filter arguments, packed in a single string suitable for the 'features' argument
    of an OpenLayers tile request. The format is currently

      <category_slug>|<subcategory_slug>|<map_source_slug>|<keywords>

    Where category_slug, subcategory_slug and map_source_slug may be empty strings, and keywords
    is a url quoted, space separated list of search keywords.
    '''
    def __init__(self, features_string = ''):
        self.features_string = features_string

    def parse_features(self):
        '''
        f: features, in this case a list of category_slug, subcategory_slug, map_source_slug
        and keywords separated by |.
        '''
        category = None
        subcategory = None
        map_source = None
        keywords = ''

        features_split = self.features_string.split('|')
        if len(features_split) > 0:
            category_id = features_split[0]
            if category_id:
                category = get_object_or_404(Category, id = category_id)

            if len(features_split) > 1:
                subcategory_id = features_split[1]
                if subcategory_id:
                    subcategory = get_object_or_404(SubCategory, id = subcategory_id)

                if len(features_split) > 2:
                    keywords = features_split[2]

        return (category, subcategory, map_source, keywords)

    def make_features(self, category, subcategory, map_source, keywords):
        self.features_string = '%s|%s|%s' % (category.id if category else '',
                                             subcategory.id if subcategory else '',
                                             keywords)


class OpenLayersTileArguments(object):
    '''
    The set of arguments in a standard OpenLayers tile request.
    This class holds arguments about zoom level, coordinates of the tile and "features", that
    is a free string that can be used to filter, for example.
    It can parse the arguments from the url and also generate the features string.
    '''
    def __init__(self, request):
        arguments_form = OpenLayersTileArgumentsForm(request.GET)
        if arguments_form.is_valid():
            self.is_valid = True
            self.left = arguments_form.cleaned_data.get('left', None)
            self.right = arguments_form.cleaned_data.get('right', None)
            self.top = arguments_form.cleaned_data.get('top', None)
            self.bottom = arguments_form.cleaned_data.get('bottom', None)
            features_string = arguments_form.cleaned_data['features']
            features = OpenLayersFeatures(features_string)
            (self.category, self.subcategory, self.map_source, self.keywords) = features.parse_features()
        else:
            self.is_valid = False
