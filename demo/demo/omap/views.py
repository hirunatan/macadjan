# Create your views here.

from macadjan.views import EntitiesText, EntitiesList, Entity
from macadjan.views import EntitiesKml, EntitiesGeoRSS
from .models import SampleEntity

class SampleEntitiesText(EntitiesText):
    model = SampleEntity

class SampleEntitiesList(EntitiesList):
    model = SampleEntity

class SampleEntitiesKml(EntitiesKml):
    model = SampleEntity

class SampleEntitiesGeoRSS(EntitiesGeoRSS):
    model = SampleEntity

class SampleEntity(Entity):
    model = SampleEntity

