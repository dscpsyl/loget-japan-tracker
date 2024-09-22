from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from .models import LoGetCards


def index(request):
    return HttpResponse("Hello, world. You're at the tracker index.")

def tracker(request):
    cards = LoGetCards.objects.all()
    context = {'cards': cards,}
    return render(request, 'tracker/index.html', context)

def user(request):
    return HttpResponse("Hello, world. You're at the tracker user.")
