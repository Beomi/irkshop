from django import forms
from address.forms import AddressField


class AddressForm(forms.Form):
    address = AddressField(required=True)
    AdditionalAddress = forms.CharField(max_length=255, required=True)
    AdditionalOptioin = forms.CharField(max_length=255, label='Order Options', required=False)