from django.db import models


class User(models.Model):
    UserEmail = models.CharField(max_length=100, primary_key=True)
    UserPassword = models.CharField(max_length=256)
    UserName = models.CharField(max_length=100)
    UserPhoneNumber = models.CharField(max_length=20)
    IsBusiness = models.BooleanField(default=False)


class Movie(models.Model):
    MovieId = models.AutoField(primary_key=True)
    MovieName = models.CharField(max_length=100)
    MovieDuration = models.PositiveIntegerField()


class Event(models.Model):
    EventId = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    EventAddress = models.CharField(max_length=100)
    AvailableTickets = models.PositiveIntegerField()
    TotalTickets = models.PositiveIntegerField()
    EventDate = models.DateTimeField()
    MovieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
    EventWebsite = models.CharField(max_length=100)


class Reservation(models.Model):
    ReservationId = models.AutoField(primary_key=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    EventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    TicketsReserved = models.PositiveIntegerField()


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

