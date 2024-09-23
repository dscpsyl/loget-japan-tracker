import json
import random as rand

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import LoginForm
from .forms import SignupForm
from .models import LoGetCards
from .models import LoGetUsers


def index(request):
    """

    :param request: 

    """
    if request.user.is_authenticated:
        return redirect("tracker:tracker")

    cardsImgs = LoGetCards.objects.values_list("Img", flat=True)
    randImgs = rand.sample(list(cardsImgs), 6)

    context = {
        "imgs": randImgs,
        "loginview": "tracker:login",
        "signupview": "tracker:signup",
    }

    return render(request, "tracker/index.html", context)


@login_required
def tracker(request):
    """

    :param request: 

    """
    user = request.user
    userCards = LoGetUsers.objects.get(user=user).CardsColleted["collected"]
    userCardIds = [int(card) for card in userCards]

    cards = LoGetCards.objects.all()
    context = {
        "cards": cards,
        "collected": userCardIds,
        "username": request.user.username,
        "logoutview": "tracker:logout",
        "userview": "tracker:settings",
    }
    return render(request, "tracker/tracker.html", context)


@login_required
def processCardAction(request):
    """

    :param request: 

    """
    if request.method == "POST":
        data = json.loads(request.body)
        div_id = data.get("div_id")
        action = data.get("action")

        user = request.user
        userCards = LoGetUsers.objects.get(user=user).CardsColleted["collected"]

        if action == "add":
            if div_id not in userCards:
                userCards.append(div_id)
        elif action == "remove":
            if div_id in userCards:
                userCards.remove(div_id)

        LoGetUsers.objects.filter(user=user).update(
            CardsColleted={"collected": userCards}
        )

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "failed"}, status=400)


def signupView(request):
    """

    :param request: 

    """
    if request.user.is_authenticated:
        return redirect("tracker:tracker")

    form = SignupForm()
    context = {"form": form, "failed": False}

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tracker:success", t="signup")
        else:
            context["failed"] = True
            return render(request, "tracker/signup.html", context)

    return render(request, "tracker/signup.html", context)


def success(request, t):
    """

    :param request: param t:
    :param t: 

    """
    if request.user.is_authenticated:
        return redirect("tracker:tracker")

    context = {"t": t}

    return render(request, "tracker/success.html", context)


def loginView(request):
    """

    :param request: 

    """
    if request.user.is_authenticated:
        return redirect("tracker:tracker")

    form = LoginForm()
    context = {"form": form, "failed": False}

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                existingUser = LoGetUsers.objects.filter(user=user)
                if not existingUser:
                    LoGetUsers(user=user, CardsColleted={"collected": []}).save()
                return redirect("tracker:tracker")

        context["failed"] = True

    return render(request, "tracker/login.html", context)


@login_required
def logoutView(request):
    """

    :param request: 

    """
    logout(request)
    return redirect("tracker:success", t="logout")


@login_required
def settings(request):
    """

    :param request: 

    """
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # Save the new password
            # Prevent user from being logged out after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("tracker:settings")
        else:
            messages.error(request, "Please correct the error below.")

    form = PasswordChangeForm(user=request.user)
    context = {"form": form, "username": request.user.username}

    return render(request, "tracker/settings.html", context)


@login_required
def exportData(request):
    """

    :param request: 

    """
    user = request.user
    collected = LoGetUsers.objects.get(user=user).CardsColleted
    cards = json.dumps(collected)

    return HttpResponse(
        cards,
        headers={
            "Content-Type": "text/plain",
            "Content-Disposition": 'attachment; filename="collectedcards.json"',
        },
    )


@login_required
def deleteDaccount(request):
    """

    :param request: 

    """
    if request.method == "POST":
        request.user.delete()
        return redirect("tracker:success", t="delete")

    return render(request, "tracker/deleteConfirmation.html")
