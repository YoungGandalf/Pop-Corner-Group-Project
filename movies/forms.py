from django import forms
from django.forms import EmailInput, PasswordInput, CheckboxInput, ModelForm, NumberInput, TextInput, NumberInput, \
    DateTimeInput, URLInput

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


# Form created for adding reservation information: Contains all relevant fields, widgets set for specific inputs,
# and labels
class ReservationForm(ModelForm):
    TicketsReserved = forms.IntegerField(widget=TextInput, label='Tickets Reserved')
    temp = forms.IntegerField(widget=TextInput, label='temp')  # Temporary input to hold the current event ID

    class Meta:
        model = Reservation
        fields = ["TicketsReserved", "temp"]


class EventForm(ModelForm):
    # EventId = forms.AutoField(max_length=100, label='EventID')
    # BusinessOwner = forms.ForeignKey(MyUser, on_delete=models.CASCADE)
    EventName = forms.CharField(widget=TextInput, max_length=100, label="Name of Event")
    EventAddress = forms.CharField(widget=TextInput, max_length=100, label='Address of Event')
    # can place auto increment to decrement when bought
    AvailableTickets = forms.IntegerField(widget=NumberInput, label="Tickets Available")
    TotalTickets = forms.IntegerField(widget=NumberInput, label="Total Tickets")
    EventDate = forms.DateTimeField(widget=DateTimeInput, label="Event Date")
    # what movie to watch. So movies name/selection
    # MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
    EventWebsite = forms.URLField(widget=URLInput, max_length=100, label='Website Url')

    class Meta:
        model = Event
        fields = ["EventName", "EventAddress", "AvailableTickets", "TotalTickets", "EventDate", "EventWebsite"]


class EventForm(ModelForm):
    # EventId = forms.AutoField(max_length=100, label='EventID')
    # BusinessOwner = forms.ForeignKey(MyUser, on_delete=models.CASCADE)
    EventName = forms.CharField(widget=TextInput, max_length=100, label="Name of Event")
    EventAddress = forms.CharField(widget=TextInput, max_length=100, label='Address of Event')
    # can place auto increment to decrement when bought
    AvailableTickets = forms.IntegerField(widget=NumberInput, label="Tickets Available")
    TotalTickets = forms.IntegerField(widget=NumberInput, label="Total Tickets")
    EventDate = forms.DateTimeField(widget=DateTimeInput, label="Event Date")
    # what movie to watch. So movies name/selection
    # MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
    EventWebsite = forms.URLField(widget=URLInput, max_length=100, label='Website Url')

    class Meta:
        model = Event
        fields = ["EventName", "EventAddress", "AvailableTickets", "TotalTickets", "EventDate", "EventWebsite"]
