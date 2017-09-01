from django import forms
from address.forms import AddressField

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'ingress_mail',
            'ingress_agent_name',
            'is_shipping',
            'address',
            'additional_address',
            'custom_order',
        ]

    ingress_mail = forms.CharField(max_length=200, required=True)
    ingress_agent_name = forms.CharField(max_length=200, required=True)
    is_shipping = forms.widgets.boolean_check(v=None)
    address = AddressField(required=False)
    additional_address = forms.CharField(max_length=255, required=False)
    custom_order = forms.CharField(max_length=255, label='Order Options', required=False)
