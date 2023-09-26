# forms.py

from django import forms

class URLForm(forms.Form):
    # This is an empty form since URLs will be fetched from a JSON file
    pass