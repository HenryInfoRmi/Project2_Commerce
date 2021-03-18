from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
import os 
from .models import User, auct_list, category
from django.forms.widgets import ClearableFileInput
from datetime import datetime
from . import forms






        


def index(request):
    cat_fil = request.GET.get('category', '')
    if cat_fil:
        id_cat = category.objects.get(name_cat=cat_fil)
        return render(request, "auctions/index.html", {
            "aucts": auct_list.objects.filter(categ_act=id_cat.id),
            "diret": os.path.dirname(os.path.realpath(__file__)),
            'categorys': category.objects.all()
        })
    else:
        user_request = request.GET.get('user_request', '')
        if user_request == 'my_items':
            if request.user.is_authenticated:
                return render(request, "auctions/index.html", {
                    "aucts": auct_list.objects.filter(name_user=request.user.id),
                    "diret": os.path.dirname(os.path.realpath(__file__)),
                    'categorys': category.objects.all()
                })
            else:
                return HttpResponseRedirect(reverse("login"))     

        return render(request, "auctions/index.html", {
            "aucts": auct_list.objects.all(),
            "diret": os.path.dirname(os.path.realpath(__file__)),
            'categorys': category.objects.all()
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
                "message": "Invalid username and/or password.",
                'categorys': category.objects.all()
            })
    else:
        return render(request, "auctions/login.html", {
            'categorys': category.objects.all()
        })


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
                "message": "Passwords must match.",
                'categorys': category.objects.all()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                'categorys': category.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{
            'categorys': category.objects.all()
        })


def add(request):
    if request.method == "POST":
        form = forms.NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = auct_list()
            new_item.name_act = form.cleaned_data["name_act"]
            new_item.price_act = form.cleaned_data["price_act"]
            new_item.picture_act = form.cleaned_data["picture_act"]
            new_item.date_act = datetime.now()
            new_item.desc_act = form.cleaned_data["desc_act"]
            new_item.categ_act = form.cleaned_data["categ_act"]
            new_item.name_user = request.user.id
            new_item.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/add.html",{
                "form": form,
                "faled": 'fail',
                'categorys': category.objects.all()
            })
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else:
        new_form = forms.NewItemForm()
        return render(request, "auctions/add.html",{
            "form": new_form,
            'categorys': category.objects.all()
        })