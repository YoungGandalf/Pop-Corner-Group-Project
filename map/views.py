from django.shortcuts import render
from movies import forms as movies_forms

def map(request):
    Events = movies_forms.Event.objects.filter()
    context = {
        'Events': Events,
    }
    return render(request, 'map/index.html', context=context)
