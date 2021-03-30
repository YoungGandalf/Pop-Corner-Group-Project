from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'movies/index.html')


def signup(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        fs = form.save(commit=False)
        UserEmail = form.cleaned_data.get('UserEmail')
        UserPassword = form.cleaned_data.get('UserPassword')
        UserName = form.cleaned_data.get('UserName')
        UserPhoneNumber = form.cleaned_data.get('UserPhoneNumber')
        IsBusiness = form.cleaned_data.get('IsBusiness')

        if UserPassword == UserPassword:
            try:
                user = User.objects.get(username=UserName)  # if able to get, user exists and must try another username
                context = {'form': form,
                           'error': 'The username you entered has already been taken. Please try another username.'}
                return render(request, 'movies/signup.html', context)
            except User.DoesNotExist:
                user = User.objects.create_user(UserName, password=UserPassword,
                                                email=UserEmail)
                user.save()

                login(request, user)

                fs.user = request.user

                fs.save()
                form = UserForm(None)
                context = {'form': form}
                return render(request, 'movies/signup.html', context)

    else:
        context = {'form': form}
        return render(request, 'movies/signup.html', context)
