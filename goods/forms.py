from django import forms
from .models import UserInfo
from address.forms import AddressField


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'address',
        ]

    address = AddressField()