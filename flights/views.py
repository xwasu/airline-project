from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger, Airport

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render (request, "flights/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "flights/login.html")

def logout_view(request):
    logout(request)
    return render(request, "flights/login.html", {
        "message": "Logged out."
    })

def airports(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "flights/airports.html", {
        "airports": Airport.objects.all()
    })

def passengers(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "flights/passengers.html", {
        "passengers": Passenger.objects.all()
    })
    
def flight(request, flight_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

def unbook(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.remove(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))