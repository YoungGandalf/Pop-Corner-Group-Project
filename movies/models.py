from django.db import models
# Validators: Validate the fields
from .validators import *


class MyUser(models.Model):
    UserEmail = models.EmailField(max_length=100, primary_key=True, validators=[validate_name_length])
    UserPassword = models.CharField(max_length=256, validators=[validate_password_length, validate_password_digit,
                                                                validate_password_uppercase])
    UserName = models.CharField(max_length=100, validators=[validate_name_length, validate_username_alphadigits])
    UserPhoneNumber = models.CharField(max_length=20, validators=[validate_phonenumber])
    IsBusiness = models.BooleanField(default=False)


class Movie(models.Model):
    MovieId = models.AutoField(primary_key=True)
    MovieName = models.CharField(max_length=100)
    MovieDuration = models.IntegerField()


class Event(models.Model):
    EventId = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    EventAddress = models.CharField(max_length=100)
    AvailableTickets = models.IntegerField()
    TotalTickets = models.IntegerField()
    EventDate = models.DateTimeField()
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
    EventWebsite = models.CharField(max_length=100)


class Reservation(models.Model):
    ReservationId = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    EventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    TicketsReserved = models.IntegerField()


class Watchlist(models.Model):
    WatchlistId = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Payment(models.Model):
    PaymentId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    CardNumber = models.CharField(max_length=256, validators=[validate_card_number])
    ExpDate = models.CharField(max_length=256, validators=[validate_expiration_date])
    SecCode = models.CharField(max_length=256, validators=[validate_security_code])
    Address = models.CharField(max_length=100)
    ZipCode = models.CharField(max_length=10, validators=[validate_zip_code])
