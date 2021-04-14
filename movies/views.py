from django.shortcuts import render, redirect
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
            return render(request, 'movies/index.html', context)

        else:
            # Reload page if form is not valid
            context = {'form': form}
            return render(request, 'movies/payment.html', context)

    # User must be logged into their account to add a credit card
    else:
        messages.info(request, "You must login to add payment information")
        return redirect('/login')
