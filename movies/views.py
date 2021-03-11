from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
#from movies.models import PopCorner


def index(request):

    return render(request, 'movies/index.html')
