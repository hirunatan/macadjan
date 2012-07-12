# -*- coding: utf-8 -*-

from django import forms

class ParamsValidationForm(forms.Form):
    lat = forms.FloatField(required=False)
    lon = forms.FloatField(required=False)
    cat = forms.IntegerField(required=False)
    subcat = forms.IntegerField(required=False)
    zoom = forms.IntegerField(required=False)

class OpenLayersTileArgumentsForm(forms.Form):
    '''
    Process filters for the markers in a map tile.
    '''
    bbox = forms.CharField(required = True)          # contain 'left,right,top,bottom'
    features = forms.CharField(required = True)      # features

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
