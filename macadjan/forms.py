# -*- coding: utf-8 -*-

from django import forms

class MapArgumentsForm(forms.Form):
    '''
    Process arguments for map views.
    '''
    src = forms.CharField(required = False)     # map source
    kw = forms.CharField(required = False)      # search keywords
    lon = forms.FloatField(required = False)    # initial longitude
    lat = forms.FloatField(required = False)    # initial latitude
    z = forms.IntegerField(required = False)    # initial zoom (from 1=whole earth to 16=max zoom).
    bl = forms.FloatField(required = False)     # map bounds left
    br = forms.FloatField(required = False)     # map bounds right
    bt = forms.FloatField(required = False)     # map bounds top
    bb = forms.FloatField(required = False)     # map bounds bottom


class ListArgumentsForm(forms.Form):
    '''
    Process arguments for entity list views.

    The bbox argument is expanded to left, right, top and bottom in clean().
    '''
    cat = forms.IntegerField(required = False)    # category id
    subcat = forms.IntegerField(required = False) # subcategory id
    src = forms.CharField(required = False)       # map source id
    kw = forms.CharField(required = False)        # search keywords
    bbox = forms.CharField(required = False)      # contain 'left,right,top,bottom'

    def clean(self):
        cleaned_data = self.cleaned_data
        bbox = cleaned_data.get("bbox")

        if bbox:
            bbox_split = bbox.split(',')
            if not len(bbox_split) == 4:
                msg = u"Bbox is incorrectly formatted, must contain 4 comma-separated coordinates"
                self._errors["bbox"] = self.error_class([msg])

            for i, name in enumerate(['left', 'bottom', 'right', 'top']):
                coord = bbox_split[i]
                try:
                    float(coord)
                    cleaned_data[name] = coord
                except ValueError:
                    msg = u"Can't convert '%s' to float" % coord
                    self._errors["bbox"] = self.error_class([msg])
        else:
            cleaned_data['left'] = None
            cleaned_data['right'] = None
            cleaned_data['top'] = None
            cleaned_data['bottom'] = None

        return cleaned_data

