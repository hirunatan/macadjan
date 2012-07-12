# Create your views here.

from macadjan.views import EntitiesText, EntitiesList
from .models import SampleEntity

class SampleEntitiesText(EntitiesText):
    model = SampleEntity

class SampleEntitiesList(EntitiesList):
    model = SampleEntity

