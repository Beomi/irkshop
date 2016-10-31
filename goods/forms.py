from django import forms
from address.forms import AddressField


class OrderForm(forms.Form):
    is_shipping = forms.widgets.boolean_check(v=None)
    address = AddressField(required=False)
    AdditionalAddress = forms.CharField(max_length=255, required=False)

    OrderOptioin = forms.CharField(max_length=255, label='Order Options', required=False)
