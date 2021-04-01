from django import forms
from django.forms import EmailInput, PasswordInput, CheckboxInput, ModelForm

from movies.models import MyUser


# Form created for User Sign Up: Contains all relevant fields, widgets set for specific inputs, and labels
class UserForm(ModelForm):
    UserEmail = forms.EmailField(widget=EmailInput, label='Email')
    UserPassword = forms.CharField(widget=PasswordInput, label='Password')
    UserName = forms.CharField(max_length=100, label='Username')
    UserPhoneNumber = forms.CharField(max_length=20, label='Phone Number')
    # The IsBusiness checkbox does not have to be checked off so required is set to false (all other fields are
    # required)
    IsBusiness = forms.BooleanField(widget=CheckboxInput, required=False, label='Is A Business?')

    class Meta:
        model = MyUser
        fields = ["UserEmail", "UserPassword", "UserName", "UserPhoneNumber", "IsBusiness"]
