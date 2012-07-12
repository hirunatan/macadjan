# Create your views here.

from macadjan.views import Entities
from .models import Entity

class EcozoomEntities(Entities):
    model = Entity
