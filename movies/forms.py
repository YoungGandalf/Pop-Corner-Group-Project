from django import forms
from django.forms import EmailInput, PasswordInput, CheckboxInput, ModelForm

from movies.models import MyUser, Payment


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


# Form created for adding payment information: Contains all relevant fields, widgets set for specific inputs, and labels
class PaymentForm(ModelForm):

    CardNumber = forms.CharField(max_length=20, label='Card Number')
    ExpDate = forms.CharField(max_length=5, label='Expiration Date (mm/yy)')
    SecCode = forms.CharField(max_length=3, label='Security Code')
    Address = forms.CharField(max_length=100, label='Billing Address')
    ZipCode = forms.CharField(max_length=5, label='Zip Code')

    class Meta:
        model = Payment
        fields = ["CardNumber", "ExpDate", "SecCode", "Address", "ZipCode"]
