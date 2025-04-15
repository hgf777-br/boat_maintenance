from django import forms

from .models import Maintenance, Periodic


class MaintenanceForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['boat'].widget.attrs = {'class': 'form-select', 'placeholder': '#', 'autofocus':''}
        self.fields['boat'].empty_label = None
        self.fields['sector'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['description'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['due_date'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['schedule_date'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['technician'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['technician'].empty_label = None
        self.fields['obs'].widget.attrs = {'class': 'form-control', 'placeholder': '#', 'style': 'height: 100px'} 

    class Meta:
        model = Maintenance
        fields = (
            'boat',
            'sector',
            'description',
            'due_date',
            'schedule_date',
            'technician',
            'obs'
        )


class PeriodicForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['boat'].widget.attrs = {'class': 'form-select', 'placeholder': '#', 'autofocus':''}
        self.fields['boat'].empty_label = None
        self.fields['sector'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['periodicity'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['periodicity_day'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['periodicity_week_day'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['periodicity_month'].widget.attrs = {'class': 'form-select', 'placeholder': '#'}
        self.fields['description'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}

    class Meta:
        model = Periodic
        fields = (
            'boat',
            'sector',
            'description',
            'periodicity',
            'periodicity_day',
            'periodicity_week_day',
            'periodicity_month',
        )
