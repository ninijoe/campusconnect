# social_network/views.py
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.shortcuts import redirect
from django.middleware import csrf
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import datetime
import logging
from django.contrib import messages
from .models import User

@login_required
def index(request):
    user = request.user
    return render(request, 'social_network/index.html', {'user': user})


def my_profile(request):
    return render(request, 'social_network/my_profile.html')

def discover(request):
    return render(request, 'social_network/discover.html')

def settings(request):
    return render(request, 'social_network/settings.html')


def login_view(request):

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "social_network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:

        return render(request, "social_network/login.html", {'csrf_token': csrf.get_token(request)})


def signup(request):
    if request.method == "POST":
        
        # Takes in the user username and email submitted in the signup form
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "social_network/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "social_network/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, 'social_network/index.html')
    else:
        return render(request, "social_network/signup.html", {'csrf_token': csrf.get_token(request)})

# Create your views here.
