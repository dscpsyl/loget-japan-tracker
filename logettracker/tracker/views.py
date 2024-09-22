from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout 

from .forms import UserCreationForm, LoginForm
from .models import LoGetCards, LoGetUsers

import random as rand

def index(request):
    if request.user.is_authenticated:
        return redirect('tracker:tracker')
    
    cardsImgs = LoGetCards.objects.values_list('Img', flat=True)
    randImgs = rand.sample(list(cardsImgs), 6)
    
    context = {'imgs': randImgs,
                'loginview': 'tracker:login',
                'signupview': 'tracker:signup'}

    return render(request, 'tracker/index.html', context)

def tracker(request):
    if not request.user.is_authenticated:
        return redirect('tracker:index')
    
    cards = LoGetCards.objects.all()
    context = {'cards': cards,
               'username': request.user.username,
               "logoutview": 'tracker:logout',
               'userview': 'tracker:user'}
    return render(request, 'tracker/tracker.html', context)


def signupView(request):
    form = UserCreationForm()
    context = {'form': form,
               'failed': False}
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:success', t='signup')
        else:
            context['failed'] = True
            return render(request, 'tracker/signup.html', context)
        
    return render(request, 'tracker/signup.html', context)

def success(request, t):
    context = {'t': t}
    
    return render(request, 'tracker/success.html', context)

def loginView(request):
    form = LoginForm()
    context = {'form': form,
                "failed": False}
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                existingUser = LoGetUsers.objects.filter(user=user)
                if not existingUser:
                    LoGetUsers(user=user, CardsColleted={'collected': []}).save()
                return redirect('tracker:tracker')
        
        context['failed'] = True
    
    return render(request, 'tracker/login.html', context)

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('tracker:success', t='logout')
    else:
        return redirect('tracker:index')

def userView(request):
    return HttpResponse("Hello, world. You're at the tracker user.")