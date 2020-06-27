from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'id': 'first_name',
        'class': 'form-control',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'id': 'last_name',
        'class': 'form-control',
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'youremail@example.com',
        'id': 'email',
        'class': 'form-control',
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'id': 'street_address',
        'class': 'form-control',
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or Suite',
        'id': 'apartment_address',
        'class': 'form-control',
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'id': 'country',
            'class': 'custom-select d-block w-100',
        }
    ))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'zip_code',
        'class': 'form-control',
    }))
