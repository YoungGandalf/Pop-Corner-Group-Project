from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
# from movies.models import PopCorner

from django.urls import reverse
from movies.models import User


def index(request):
    return render(request, 'movies/index.html')


def signup(request):
    Users = User.objects.filter()
    context = {
        'Users': Users,
    }
    return render(request, 'movies/signup.html', context=context)


def add(request):
    UserEmail = request.POST['email']
    UserPassword = request.POST['password']
    UserName = request.POST['name']
    UserPhoneNumber = request.POST['number']
    if request.POST.get("isbusiness") == "clicked":
        IsBusiness = True
    else:
        IsBusiness = False
    Users = User(UserEmail=UserEmail,UserPassword=UserPassword,
                 UserName=UserName,UserPhoneNumber=UserPhoneNumber,IsBusiness=IsBusiness)
    Users.save()
    return HttpResponseRedirect(reverse('signup'))
