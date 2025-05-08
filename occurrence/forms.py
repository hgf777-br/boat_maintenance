from datetime import datetime
from django import forms

from .models import CheckInOut, Occurrence


class OccurrenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['boat'].widget.attrs = {'class': 'form-select', 'placeholder': '#', 'autofocus': ''}
        self.fields['boat'].empty_label = None
        self.fields['sector'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['description'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['hour_meter'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['date'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['date'].initial = datetime.now().date()
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
            'hour_meter',
            'obs'
        )
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }


class CheckInOutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['boat'].widget.attrs = {'class': 'form-select', 'placeholder': '#', 'autofocus': ''}
        self.fields['boat'].empty_label = None
        self.fields['checkin_date'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['checkin_date'].initial = datetime.now().date()
        self.fields['checkin_hour_meter'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['checkin_obs'].widget.attrs = {'class': 'form-control',
                                                   'placeholder': '#', 'style': 'height: 100px'}
        self.fields['checkout_date'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['checkout_date'].initial = datetime.now().date()
        self.fields['checkout_hour_meter'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['checkout_obs'].widget.attrs = {'class': 'form-control',
                                                    'placeholder': '#', 'style': 'height: 100px'}
        if self.instance:
            print(f'CheckInOut ID: {self.instance.id}')

    class Meta:
        model = CheckInOut
        fields = (
            'boat',
            'checkin_date',
            'checkin_hour_meter',
            'checkin_obs',
            'checkout_date',
            'checkout_hour_meter',
            'checkout_obs',
        )
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }
