# Create your views here.

from macadjan.views import Entities
from .models import SampleEntity

class SampleEntities(Entities):
    model = SampleEntity
