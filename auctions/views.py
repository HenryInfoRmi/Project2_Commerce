from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
import os 
from .models import User, auct_list
from django.forms.widgets import ClearableFileInput
from datetime import datetime
from . import forms






        


def index(request):
    return render(request, "auctions/index.html", {
        "aucts": auct_list.objects.all(),
        "diret": os.path.dirname(os.path.realpath(__file__))
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add(request):
    if request.method == "POST":
        form = forms.NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/add.html",{
                "form": form,
                "faled": 'fail'
            })
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        new_form = forms.NewItemForm()
        return render(request, "auctions/add.html",{
            "form": new_form
        })