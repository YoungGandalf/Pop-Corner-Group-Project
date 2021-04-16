from django.shortcuts import render, redirect
from .forms import UserForm, EventForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import MyUser, Event


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
