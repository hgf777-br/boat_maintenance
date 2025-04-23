from django import forms

from .models import Occurrence


class OccurrenceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['boat'].widget.attrs = {'class': 'form-select', 'placeholder': '#', 'autofocus': ''}
        self.fields['boat'].empty_label = None
        self.fields['sector'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['description'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['engine_hours'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['date'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['obs'].widget.attrs = {'class': 'form-control', 'placeholder': '#', 'style': 'height: 100px'}
        if self.instance:
            print(f'Occurrence ID: {self.instance.id}')

    class Meta:
        model = Occurrence
        fields = (
            'date',
            'description',
            'boat',
            'sector',
            'engine_hours',
            'obs'
        )
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }
