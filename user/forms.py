from django import forms

from .models import User


class UserCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': '#', 'autofocus': ''}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'required': '', 'placeholder': '#'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'required': '', 'placeholder': '#'}
        self.fields['profile'].widget.attrs = {'class': 'form-select'}
        self.fields['theme'].widget.attrs = {'class': 'form-select'}
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '#'})

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'profile',
            'theme',
            'password',
        )


class UserUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': '#'}
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'required': '', 'placeholder': '#'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'required': '', 'placeholder': '#'}
        self.fields['profile'].widget.attrs = {'class': 'form-select'}
        self.fields['theme'].widget.attrs = {'class': 'form-select'}

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'profile',
            'theme',
        )
