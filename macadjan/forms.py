# -*- coding: utf-8 -*-

from django import forms

class ParamsValidationForm(forms.Form):
    lat = forms.FloatField(required=False)
    lon = forms.FloatField(required=False)
    cat = forms.IntegerField(required=False)
    subcat = forms.IntegerField(required=False)
    zoom = forms.IntegerField(required=False)

