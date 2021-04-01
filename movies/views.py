from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login


def index(request):
    return render(request, 'movies/index.html')


# SignUp View
def signup(request):
    # Initialize form with the data from the site or none
    form = UserForm(request.POST or None)

    # If the form is valid
    if form.is_valid():
        fs = form.save(commit=False) # save the information from the form

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
            return render(request, 'movies/signup.html', context) # return to same signup page

        # When the user does not arleady exist in the system
        except User.DoesNotExist:
            # Create a user with django's user model and save
            user = User.objects.create_user(UserName, password=UserPassword, email=UserEmail)
            user.save()

            login(request, user) # May want to remove this since it automatically logs in the user

            # Save the form
            fs.user = request.user
            fs.save()

            form = UserForm(None) # clear the UserForm so reloading will bring up a blank form
            context = {'form': form}
            return render(request, 'movies/signup.html', context) # return to same signup page

    else:
        context = {'form': form}
        return render(request, 'movies/signup.html', context) # return to same signup page
