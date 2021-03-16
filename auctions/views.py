from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os 
from .models import User, auct_list
from django import forms
from django.forms.widgets import ClearableFileInput


class NewItemForm(forms.ModelForm):
    picture_act = forms.ImageField(widget=ClearableFileInput, label="Image")
    
    class Meta:
        model = auct_list
        fields = '__all__'#['name_act', 'price_act', 'desc_act', 'picture_act']
        labels = {
            'name_act':'Name product',
            'price_act':'Price',
            'desc_act':'Description'
        }
        


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
    if request.method == "POT":
        
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
        else:
            return render(request, "auctions/add.html",{
                "form": form,
                "faled": 'fail'
            })
        pass
    if not request.user.is_authenticated:
        HttpResponseRedirect('/login/')
    else:
        return render(request, "auctions/add.html",{
            "form": NewItemForm()
        })