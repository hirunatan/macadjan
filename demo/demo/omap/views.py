# Create your views here.

from macadjan.views import EntitiesText, EntitiesList, Entity
from .models import SampleEntity

class SampleEntitiesText(EntitiesText):
    model = SampleEntity

class SampleEntitiesList(EntitiesList):
    model = SampleEntity

class SampleEntity(Entity):
    model = SampleEntity

