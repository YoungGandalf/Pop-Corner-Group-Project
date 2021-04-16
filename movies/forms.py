from django import forms
from django.forms import EmailInput, PasswordInput, CheckboxInput, ModelForm, TextInput, NumberInput, DateTimeInput,\
    URLInput

from .models import *


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


class EventForm(ModelForm):
    # EventId = forms.AutoField(max_length=100, label='EventID')
    # BusinessOwner = forms.ForeignKey(MyUser, on_delete=models.CASCADE)
    EventAddress = forms.CharField(widget=TextInput, max_length=100, label='Address of Event')
    # can place auto increment to decrement when bought
    AvailableTickets = forms.IntegerField(widget=NumberInput, label="Tickets Available")
    TotalTickets = forms.IntegerField(widget=NumberInput, label="Total Tickets")
    EventDate = forms.DateTimeField(widget=DateTimeInput, label="Event Date")
    # what movie to watch. So movies name/selection
    # MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
    EventWebsite = forms.CharField(widget=URLInput, max_length=100, label='Website Url')

    class Meta:
        model = Event
        fields = ["EventAddress", "AvailableTickets", "TotalTickets", "EventDate", "EventWebsite"]
