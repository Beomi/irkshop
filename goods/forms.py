from django import forms
from .models import UserInfo
from address.forms import AddressField


class UserInfoForm(forms.Form):

    address = AddressField()