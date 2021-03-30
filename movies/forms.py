from django import forms
from django.forms import EmailInput, PasswordInput, CheckboxInput, ModelForm

from movies.models import User


class UserForm(ModelForm):
    UserEmail = forms.EmailField(widget=EmailInput, label='Email')
    UserPassword = forms.CharField(widget=PasswordInput, label='Password')
    UserName = forms.CharField(max_length=100, label='Username')
    UserPhoneNumber = forms.CharField(max_length=20, label='Phone Number')
    IsBusiness = forms.BooleanField(widget=CheckboxInput, required=False, label='Is A Business?')

    class Meta:
        model = User
        fields = ["UserEmail", "UserPassword", "UserName", "UserPhoneNumber", "IsBusiness"]
