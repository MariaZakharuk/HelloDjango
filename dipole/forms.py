from django import forms

class PointForm(forms.Form):
    x = forms.FloatField()
    y = forms.FloatField()