from django import forms
from .models import Boat


class BoatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': '#', 'autofocus': ''}
        self.fields['manufacturer'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['model'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['year_built'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['number_shares'].widget.attrs = {
            'class': 'form-control', 'min': '4', 'max': '8', 'placeholder': '#'
            }

    class Meta:
        model = Boat
        fields = (
            'name',
            'number_shares',
            'manufacturer',
            'model',
            'year_built',
        )
