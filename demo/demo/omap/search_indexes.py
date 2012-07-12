# -*- coding: utf-8 -*-

from haystack import indexes
from .models import SampleEntity

class EntityIndexes(indexes.RealTimeSearchIndex, indexes.Indexable):
    '''
    Haystack index information of SampleEntity.
    For now, we create a 'text' index with the concatenation of several fields.
    '''
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return SampleEntity

    def index_queryset(self):
        return self.get_model().objects.filter(is_active = True)

