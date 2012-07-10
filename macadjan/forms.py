# -*- coding: utf-8 -*-

from django import forms

class ParamsValidationForm(forms.Form):
    lat = forms.IntegerField(required=False)
    lon = forms.IntegerField(required=False)
    cat = forms.IntegerField(required=False)
    subcat = forms.IntegerField(required=False
