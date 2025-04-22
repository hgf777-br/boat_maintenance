from django import forms

from .models import Technician


class TechnicianForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': '#', 'autofocus': ''}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['speciality'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['company'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}

    class Meta:
        model = Technician
        fields = (
            'name',
            'email',
            'phone',
            'speciality',
            'company',
        )
