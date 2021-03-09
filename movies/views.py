from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from movies.models import PopCorner


def index(request):
    facts = PopCorner.objects.filter()
    context = {
        'movies': facts,
    }
    return render(request, 'movies/index.html', context=context)


def add(request):
    fact_text = request.POST['fact']
    image_url = request.POST['image_url']
    fact = PopCorner(text=fact_text, image_url=image_url)
    fact.save()
    return HttpResponseRedirect(reverse('index'))
