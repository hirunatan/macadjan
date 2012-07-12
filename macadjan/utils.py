# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

from superview.utils import LazyEncoder

import json

def slugify_uniquely(value, model, slugfield="slug"):
    """
    Returns a slug on a name which is unique within a model's table
    self.slug = SlugifyUniquely(self.name, self.__class__)
    """
    suffix = 0
    potential = base = slugify(value)
    if len(potential) == 0:
        potential = 'null'
    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).count():
            return potential
        # we hit a conflicting slug, so bump the suffix & try again
        suffix += 1


def to_json(iterable_obj):
    """
    Convert any iterable or list of dicts to json
    with correct serialization of Promise and datetime objects.
    """
    data = json.dumps(iterable_obj, cls=LazyEncoder, sort_keys=False)
    return mark_safe(data)

