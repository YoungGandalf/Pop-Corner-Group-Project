from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *


def index(request):
    return render(request, 'movies/index.html')


# SignUp View
def signup(request):
    # Initialize form with the data from the site or none
    form = UserForm(request.POST or None)

    # If the form is valid
    if form.is_valid():
        fs = form.save(commit=False)  # save the information from the form

        # Get fields to store in user class
        UserEmail = form.cleaned_data.get('UserEmail')
        UserPassword = form.cleaned_data.get('UserPassword')
        UserName = form.cleaned_data.get('UserName')
        UserPhoneNumber = form.cleaned_data.get('UserPhoneNumber')
        IsBusiness = form.cleaned_data.get('IsBusiness')

        # Try block includes any possible errors with duplicate usernames
        try:
            user = User.objects.get(username=UserName)  # if the user already exists then prompt again
            context = {'form': form,
                       'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'movies/signup.html', context)  # return to same signup page

        # When the user does not arleady exist in the system
        except User.DoesNotExist:
            # Create a user with django's user model and save
            user = User.objects.create_user(UserName, password=UserPassword, email=UserEmail)
            user.save()

            login(request, user)  # May want to remove this since it automatically logs in the user

            # Save the form
            fs.user = request.user
            fs.save()

            # Update the database so that the password in the database is also hashed
            MyUser.objects.filter(UserEmail=user.email).update(UserPassword=user.password)

            form = UserForm(None)  # clear the UserForm so reloading will bring up a blank form
            context = {'form': form}
            return render(request, 'movies/index.html', context)  # return to same signup page

    else:
        context = {'form': form}
        return render(request, 'movies/signup.html', context)  # return to same signup page


# Login View
def login_user(request):
    # Already Logged In
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return render(request, 'movies/index.html')

    if request.method == 'POST':
        # Gets username and password from .html and authenticates it against the database
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        # Successful Login
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect('/')
        # Unsuccessful Login
        else:
            form = AuthenticationForm(request.POST)
            messages.error(request, "The username and/or password is invalid")
            return render(request, 'movies/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'movies/login.html', {'form': form})


# Logout View
def logout_user(request):
    logout(request)
    messages.info(request, "You have logged out successfully!")
    return redirect('/')


def add_payment(request):
    # Initialize form on the page
    form = PaymentForm(request.POST or None)

    # Check if user is logged in
    if request.user.is_authenticated:

        if form.is_valid():

            # Grab current users email for foreign key in Payment object creation,
            username = request.user.get_username()
            currentUser = MyUser.objects.get(UserName=username)

            # Create new payment object and save
            payment = Payment(Owner_id=currentUser.UserEmail,
                              CardNumber=form.cleaned_data.get('CardNumber'),
                              ExpDate=form.cleaned_data.get('ExpDate'),
                              SecCode=form.cleaned_data.get('SecCode'),
                              Address=form.cleaned_data.get('Address'),
                              ZipCode=form.cleaned_data.get('ZipCode'))

            payment.save()

            # Clear the form and return to the home page
            form = PaymentForm(None)
            context = {'form': form}
            messages.info(request, "Your payment has been successfully added!")
            return render(request, 'movies/index.html', context)

        else:
            # Reload page if form is not valid
            context = {'form': form}
            return render(request, 'movies/payment.html', context)

    # User must be logged into their account to add a credit card
    else:
        messages.info(request, "You must login to add payment information")
        return redirect('/login')


# Used for the for loop in order to print out event information
def reservation(request):
    # Check if user is logged in
    if request.user.is_authenticated:

        Events = Event.objects.filter()
        Count = Event.objects.filter().count()
        context = {
            'Events': Events,
            'Count': Count,
        }
        return render(request, 'movies/reservation.html', context=context)

    # User must be logged into their account to add a reservation
    else:
        messages.info(request, "You must login to create a purchase")
        return redirect('/login')


# Add reservation to the database
def add(request):
    # Check if user is logged in
    if request.user.is_authenticated:

        # Get the list of tickets the user put in
        numTickets = request.POST.getlist('tickets')
        # Get list of IDs for each ticket
        eventID = request.POST.getlist('tempId')

        # Boolean which checks if the list of NumTickets are valid ints
        validNum = True
        # Iterate through the list of tickets and check each one in an integer
        for c in range(len(numTickets)):
            # If not an integer then set the boolean to False
            if not numTickets[c].isdigit():
                validNum = False

        # If the boolean is set to false then reprompt the user for another input
        if not validNum:
            # If it failed then reprompt the user for another input
            messages.error(request,
                           "The number of tickets you entered contains characters. Please only include integers.")
            Events = Event.objects.filter()
            context = {
                'Events': Events,
            }
            return render(request, 'movies/reservation.html', context)

        # Boolean to check if the entire array(tickets) is full of 0s
        isZeros = False
        # Count number of 0s in the array
        count0 = 0
        # Iterate through the numTickets array
        for r in range(len(numTickets)):
            # Keep a counter for the number of 0s that exist
            if int(numTickets[r]) == 0:
                count0 = count0 + 1
        # If the entire array is full of 0s then set the boolean to true
        if count0 == len(numTickets):
            isZeros = True

        # Iterate through the numTickets array
        for i in numTickets:

            # Validate the number of tickets the user placed
            if int(i) < 0:
                # If it failed then reprompt the user for another input
                messages.error(request, "The number of tickets you reserve must be a positive integer")
                Events = Event.objects.filter()
                context = {
                    'Events': Events,
                }
                return render(request, 'movies/reservation.html', context)

        # Grab current users email for foreign key in Reservation object creation,
        username = request.user.get_username()
        currentUser = MyUser.objects.get(UserName=username)

        # Set counter to keep track of indexes
        counter = 0
        # Iterate through the eventID array
        for e in eventID:

            # Get Event associated with the tempID
            currentEvent = Event.objects.get(EventId=e)

            # Need to update the Event with the current number of tickets available
            currentEvent.AvailableTickets = currentEvent.AvailableTickets - int(numTickets[counter])

            # Make sure the ticket number entered was valid
            if currentEvent.AvailableTickets < 0:
                # If it failed then reprompt the user for another input
                messages.error(request, "The number of tickets you reserved must be less than this input")
                Events = Event.objects.filter()
                context = {
                    'Events': Events,
                }
                return render(request, 'movies/reservation.html', context)

            # Save the updated information for Event in the database
            currentEvent.save()

            # If the reservation already exists then just add to the reservation (filter by event id and owner)
            if Reservation.objects.filter(EventId_id=currentEvent.EventId).filter(Owner=currentUser).exists():
                reservation = Reservation.objects.get(EventId_id=currentEvent.EventId, Owner=currentUser)
                reservation.TicketsReserved = reservation.TicketsReserved + int(numTickets[counter])
            else:
                # Create new reservation object and save it with the appropriate information
                reservation = Reservation(Owner_id=currentUser.UserEmail,
                                          EventId_id=currentEvent.EventId,
                                          TicketsReserved=int(numTickets[counter]))

            # If the current number of ticket is not equal to 0 then save the reservation
            if int(numTickets[counter]) != 0:
                # Save the updated reservation in the database
                reservation.save()
            counter = counter + 1  # Iterate counter

        # If for some reason there are no entries (full of 0s) then just reprompt to the reservation page
        if isZeros:
            # Reload page if form is not valid
            Events = Event.objects.filter()
            context = {
                'Events': Events,
            }
            return render(request, 'movies/reservation.html', context)
        else:
            # Go to the payment page to proceed
            return redirect('/payment')

    # User must be logged into their account to add a reservation
    else:
        messages.info(request, "You must login to create a purchase")
        return redirect('/login')


def event_form(request):
    # Initialize form with the data from the site or none
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        # If the form is valid
        if form.is_valid():
            # Owner user email for foreign key in Event object creation
            # this gets the MyUser primary key and stores it in ownerID
            username = request.user.get_username()
            owner_ID = MyUser.objects.get(UserName=username)

            # Get data from form to store in event class object
            eventObj = Event(
                # EventId  Need to go and get the primary key from the event field
                Owner_id=owner_ID.UserEmail,
                EventAddress=form.cleaned_data.get('EventAddress'),
                AvailableTickets=form.cleaned_data.get('AvailableTickets'),
                TotalTickets=form.cleaned_data.get('TotalTickets'),
                EventDate=form.cleaned_data.get('EventDate'),
                EventWebsite=form.cleaned_data.get('EventWebsite'),
                MovieId_id=1
            )
            eventObj.save()
            form = EventForm(None)
            context = {'form': form}
            messages.info(request, "Your event has been successfully added!")
            return render(request, 'movies/index.html', context)
        else:
            form = event_form(None)
            context = {'form': form}
            return render(request, 'movies/event.html', context)
    else:
        # Reload page if form is not valid
        context = {'form': form}
        return render(request, 'movies/event.html', context)


# Used for the for loop in order to print out reservation information
def edit_reservation(request):
    # Check if user is logged in
    if request.user.is_authenticated:

        Reservations = Reservation.objects.filter()
        username = request.user.get_username()
        owner_ID = MyUser.objects.get(UserName=username)
        Count = Reservation.objects.filter(Owner_id=owner_ID.UserEmail).count()
        context = {
            'Reservations': Reservations,
            'Count': Count,
        }
        return render(request, 'movies/edit_reservation.html', context=context)

    # User must be logged into their account to add a reservation
    else:
        messages.info(request, "You must login to create a purchase")
        return redirect('/login')


# Should take care of deleting reservation
def delete_reservation(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        if request.method == 'POST':
            res = request.POST.getlist('res')

            # Refresh back to the edit page if no boxes were selected
            if len(res) == 0:
                Reservations = Reservation.objects.filter()
                username = request.user.get_username()
                owner_ID = MyUser.objects.get(UserName=username)
                Count = Reservation.objects.filter(Owner_id=owner_ID.UserEmail).count()
                context = {
                    'Reservations': Reservations,
                    'Count': Count,
                }
                messages.info(request, "You did make any edits to your reservations.")
                return render(request, 'movies/edit_reservation.html', context=context)

            for Res in res:
                # Get Reservation to remove
                currentRes = Reservation.objects.get(ReservationId=Res)
                # Get Event to update
                currentEvent = Event.objects.get(EventId=currentRes.EventId_id)

                # Need to update the Event with the new number of tickets available
                currentEvent.AvailableTickets = currentEvent.AvailableTickets + currentRes.TicketsReserved
                # Save the updated information for Event in the database
                currentEvent.save()

                # Need to delete the reservation
                Reservation.objects.filter(ReservationId=Res).delete()

            # Refresh the page for now ( need to figure out a way to allow the user to get refunded)
            Reservations = Reservation.objects.filter()
            username = request.user.get_username()
            owner_ID = MyUser.objects.get(UserName=username)
            Count = Reservation.objects.filter(Owner_id=owner_ID.UserEmail).count()
            context = {
                'Reservations': Reservations,
                'Count': Count,
            }
            return render(request, 'movies/edit_reservation.html', context=context)

    # If user is not logged in
    else:
        messages.info(request, "You must login to create a purchase")
        return redirect('/login')


def about_us(request):
    return render(request, 'movies/about_us.html')
