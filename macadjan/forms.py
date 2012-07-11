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
                # TODO: Error
                pass

            for i, name in enumerate(['left', 'bottom', 'right', 'top']):
                coord = bbox_split[i]
                try:
                    float(bbox_split[i])
                    cleaned_date[name] = coord
                except TypeError:
                    # TODO: Error
                    pass

        return cleaned_data
