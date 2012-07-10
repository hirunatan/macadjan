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


from .forms import ParamsValidationForm

class MainPageView(CategoryResponseMixin, SubCategoriesResponseMixinView):
    template_name = "main-page.html"

    def initial_context_from_params(self):
        """
        Filter initial params from GET querystring.
        """

        initial_context = {}

        form = ParamsValidationForm(self.request.GET)
        if not form.is_valid():
            return initial_context

        initial_context.update(form.cleaned_data)
        return initial_context

    def get(self, request):
        context = {
            #"site_info":
            "initial": self.initial_context_from_params()
        }

        return self.render_to_response(self.template_name, context)
