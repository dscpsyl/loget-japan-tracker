from django.shortcuts import render
from django.http import HttpResponse


from .models import LoGetCards

import random as rand

def index(request):
    cardsImgs = LoGetCards.objects.values_list('Img', flat=True)
    randImgs = rand.sample(list(cardsImgs), 6)
    
    context = {'imgs': randImgs}

    return render(request, 'tracker/index.html', context)

def tracker(request):
    cards = LoGetCards.objects.all()
    context = {'cards': cards,
               'username': 'testuser'}
    return render(request, 'tracker/tracker.html', context)

def user(request):
    return HttpResponse("Hello, world. You're at the tracker user.")
