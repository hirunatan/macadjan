# -*- coding: utf-8 -*-

from django import forms

class MapArgumentsForm(forms.Form):
    '''
    Process arguments for map views.
    '''
    kw = forms.CharField(required = False)      # search keywords
    lon = forms.FloatField(required = False)    # initial longitude
    lat = forms.FloatField(required = False)    # initial latitude
    z = forms.IntegerField(required = False)    # initial zoom (from 1=whole earth to 16=max zoom).
    bl = forms.FloatField(required = False)     # map bounds left
    br = forms.FloatField(required = False)     # map bounds right
    bt = forms.FloatField(required = False)     # map bounds top
    bb = forms.FloatField(required = False)     # map bounds bottom


class OpenLayersTileArgumentsForm(forms.Form):
    '''
    Process filters for the markers in a map tile.
    '''
    bbox = forms.CharField(required = False)          # contain 'left,right,top,bottom'
    features = forms.CharField(required = False)      # features

    def clean(self):
        cleaned_data = self.cleaned_data
        bbox = cleaned_data.get("bbox")

        if bbox:
            bbox_split = bbox.split(',')
            if not len(bbox_split) == 4:
                msg = u"Bbox is incorrectly formatted, have to content 4 coordinates"
                self._errors["bbox"] = self.error_class([msg])

            for i, name in enumerate(['left', 'bottom', 'right', 'top']):
                coord = bbox_split[i]
                try:
                    float(bbox_split[i])
                    cleaned_data[name] = coord
                except ValueError:
                    msg = u"Can't convert to float"
                    self._errors["bbox"] = self.error_class([msg])

        return cleaned_data
