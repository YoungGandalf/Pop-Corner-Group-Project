from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mytest.models import CatFact
# Create your views here.


def index(request):
    facts = CatFact.objects.filter()
    context = {
        'facts': facts,
    }
    return render(request, 'mytest/index.html', context={})


def add(request):
    fact_text = request.POST['fact']
    image_url = request.POST['image_url']
    fact = CatFact(text=fact_text, image_url=image_url)
    fact.save()
    return HttpResponseRedirect(reverse('index'))
