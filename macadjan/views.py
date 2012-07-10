# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from superview.views import SuperView as View

from .models import Category, SubCategory
from .utils import to_json


class CategoryResponseMixin(object):
    def get_categories_query_set(self):
        return Category.objects.actives_only()

    def categories_as_json(self):
        """
        Get categories list on json format.
        """
        return to_json([obj.to_dict() \
            for obj in self.get_categories_query_set()])

class SubCategoriesResponseMixinView(object):
    def get_subcategories_query_set(self):
        return SubCategory.objects.actives_only()

    def subcategories_as_json(self):
        """
        Get subcategory list on json format.
        """
        return to_json([obj.to_dict() \
            for obj in self.get_subcategories_query_set()])


class MainPageView(CategoryResponseMixin, SubCategoriesResponseMixinView):
    template_name = "main-page.html"

    def get(self, request):
        pass

