# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from macadjan.models import Entity

class SampleEntity(Entity):
    description = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Descripción'),
            help_text = _(u'Descripción general de la entidad.'))

