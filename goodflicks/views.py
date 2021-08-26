from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import urllib.request, urllib.parse, urllib.error
import json
import random

from .helpers import imgdata, jsdecode, countries, genres, fetch, decodecountry
from .models import User
from .utils import TMDB_API_KEY, STREAMING_HEADERS

# Add login decorators for most functions; add link to template if user not logged in
# Register user, if username not taken and 
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure the passwords match (JS will check on frontend)
        password = request.POST["password"]
        confirm_password = request.POST["confirm"]
        if password != confirm_password:
            return render(request, "goodflicks/register.html", {
                "message": "Passwords must match."
            })

        country = request.POST["countries"]

        servicelist = request.POST.getlist("service")
        genrelist = request.POST.getlist("genre")

        services = ','.join(servicelist)
        genres = ','.join(genrelist)

        print(country, services, genres)


        # Check whether this will check whether the email has been taken too
        try: 
            user = User.objects.create_user(username, email, password, country=country, services=services, genres=genres)
            user.save()
        except IntegrityError:
            return render(request, "goodflicks/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        genres = fetch("genres")
        countries = fetch("countries")

        countrylist = {}
        for item in countries:
            data = decodecountry(countries[item])
            countrylist.update(data)

        countrylist = dict(sorted(countrylist.items(),key= lambda x:x[1]))

        return render(request, "goodflicks/register.html", {
            "genres": genres,
            "countrylist": countrylist
        })

def services(request):
    data = fetch('countries')
    return JsonResponse(data)

# Authenticate the user and redirect them to the index
def login_view(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "goodflicks/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "goodflicks/login.html")

# Log the user out and return them to the splash page (index)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# TEMP ROUTE to test splash page while Register needs tweaking
def splash(request):
    return render(request, "goodflicks/splash.html")

# TO-DO: Change API call to use helper functions
# Load index page, if logged in
# This will also need to forward on the page values for each carousel as a dictionary, for when JS makes API calls
def index(request):
    # countries()
    # genres()

    if request.user.is_authenticated:
        return render(request, "goodflicks/index.html")
    
    else:
        return HttpResponseRedirect(reverse("register"))

@login_required
def lists(request):
    return 0

@login_required
def profile(request, parameter=None):
    if request.method == "POST":
        data = json.loads(request.body)
        if parameter == "password":
        # STILL NEED TO UPDATE DATABASE!
        # investigate: https://docs.djangoproject.com/en/3.2/topics/auth/default/#django.contrib.auth.views.PasswordChangeView

            if data.get("oldpassword") is not None:
                user = authenticate(request, username=request.user.username, password=data["oldpassword"])
                if user is not None:
                    newpass = data["password"]
                    confirm = data["confirm"]
                    if newpass != confirm:
                        return JsonResponse({"message": "Passwords do not match."}, status=401)
                    else:
                        return JsonResponse({"message": "Data recieved."}, status=201)
                else:
                    return JsonResponse({"message": "Password authentication failed."}, status=401)
                

    else:
        genres = fetch("genres")
        countries = fetch("countries")

        countrylist = {}
        for item in countries:
            data = decodecountry(countries[item])
            countrylist.update(data)

        countrylist = dict(sorted(countrylist.items(),key= lambda x:x[1]))

        # also! turn the user's services and genres into a list

    # check that the username is the name of the user logged in
    # if user hasn't set favourite genres, run function to populate with most highly reviewed and/or most frequently viewed genres??
    # cap favourite genres at 5
        return render(request, "goodflicks/profile.html", {
            "genres": genres,
            "countrylist": countrylist,
            "countries": countries
        })

# TO-DO: change API call to use helper functions
# Change language and region so that it's not hardcoded
@login_required
def search(request):
    if request.method == "GET": 
        # Retrieve search parameter
        parameter = request.GET["q"]

        # Use TMDb multisearch to get first 20 answers
        result = urllib.request.urlopen(f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&language=en-GB&query={parameter}&page=1&include_adult=false&region=GB")
        data = jsdecode(result)
        print(f"{data}")
        posterdata = imgdata(data['results'])

        # Rewrite to grab config data from config file
        config_url = f"https://api.themoviedb.org/3/configuration?api_key={TMDB_API_KEY}"
        config_result = urllib.request.urlopen(config_url)
        config_data = config_result.read().decode()
        config_jsdata = json.loads(config_data)

        return render(request, 'goodflicks/search.html', {
            "parameter": parameter,
            "pages": data["total_pages"],
            "data": posterdata,
            "imgurl": config_jsdata["images"]["base_url"],
            "imgsize": config_jsdata["images"]["poster_sizes"][1]
        })

@login_required
def movie(request, movid):
    url = f"http://api.themoviedb.org/3/movie/{movid}?api_key={TMDB_API_KEY}"
    result = urllib.request.urlopen(url)
    data = result.read().decode()
    jsdata = json.loads(data)
    return render(request, 'goodflicks/movie.html', {
        "data": jsdata
    })

# CREATE ABOUT PAGE - this must credit TMDb, Streaming Availability and country API