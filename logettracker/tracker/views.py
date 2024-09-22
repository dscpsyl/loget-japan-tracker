from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout 

from .forms import UserCreationForm, LoginForm
from .models import LoGetCards

import random as rand

def index(request):
    if request.user.is_authenticated:
        return redirect('tracker')
    
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
               'username': 'testuser'}
    return render(request, 'tracker/tracker.html', context)


def signupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')
        else:
            return redirect('signup')
    
    form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

def signupSuccess(request):
    return render(request, 'tracker/signup_success.html') #! which will show a confirmation and redirect to login page after a few seconds

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('tracker') #! need to update it so that it loads in the user data and is only accessible to logged in users
        else:
            return redirect('login')
    
    form = LoginForm()
    return render(request, 'tracker/login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('logout_success')

def logoutSuccess(request):
    return render(request, 'tracker/logout_success.html') #! which will show a confirmation and redirect to index page after a few seconds


def userView(request):
    return HttpResponse("Hello, world. You're at the tracker user.")