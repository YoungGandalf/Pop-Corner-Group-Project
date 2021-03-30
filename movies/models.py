from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import (validate_password_length, validate_password_digit, validate_password_uppercase,
                         validate_name_length, validate_phonenumber, validate_username_alphadigits)


class User(models.Model):
    UserEmail = models.EmailField(max_length=100, primary_key=True)
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
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    EventAddress = models.CharField(max_length=100)
    AvailableTickets = models.IntegerField()
    TotalTickets = models.IntegerField()
    EventDate = models.DateTimeField()
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
    EventWebsite = models.CharField(max_length=100)


class Reservation(models.Model):
    ReservationId = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    EventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    TicketsReserved = models.IntegerField()


class Watchlist(models.Model):
    WatchlistId = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Payment(models.Model):
    PaymentId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    CardNumber = models.CharField(max_length=256)
    ExpDate = models.CharField(max_length=256)
    SecCode = models.CharField(max_length=256)
    Address = models.CharField(max_length=100)
    ZipCode = models.CharField(max_length=10)
