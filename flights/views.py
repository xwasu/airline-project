from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Flight, Passenger, Airport
from .forms import AirportForm, PassengerForm, FlightForm, RegistrationForm


# Create your views here.
def index(request):
    flight_list = Flight.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(flight_list, 3)
    try:
        flights_paginated = paginator.page(page)
    except PageNotAnInteger:
        flights_paginated = paginator.page(1)
    except EmptyPage:
        flights_paginated = paginator.page(paginator.num_pages)

    return render(request, "flights/index.html", {
        "flights": flights_paginated
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

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegistrationForm()

    return render(request, "flights/registration.html", {
        "form": form,
    })

def airports(request):
    airport_list = Airport.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(airport_list, 3)
    try:
        airports_paginated = paginator.page(page)
    except PageNotAnInteger:
        airports_paginated = paginator.page(1)
    except EmptyPage:
        airports_paginated = paginator.page(paginator.num_pages)

    return render(request, "flights/airports.html", {
        "airports": airports_paginated
    })

def passengers(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    passenger_list = Passenger.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(passenger_list, 3)
    try:
        passengers_paginated = paginator.page(page)
    except PageNotAnInteger:
        passengers_paginated = paginator.page(1)
    except EmptyPage:
        passengers_paginated = paginator.page(paginator.num_pages)

    return render(request, "flights/passengers.html", {
        "passengers": passengers_paginated
    })
    
def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except (Flight.DoesNotExist, ValueError, ValidationError):
        raise Http404("Flight does not exist or invalid flight_id.")

    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if not request.user.is_authenticated:
        raise Http404("You don't have permission to unbook this passenger.")

    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

def unbook(request, flight_id):
    if not request.user.is_authenticated:
        raise Http404("You don't have permission to unbook this passenger.")

    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.remove(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

def create_airport(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("airports"))
    else:
        form = AirportForm()

    return render(request, "flights/create_airport.html", {
        "form": form,
    })

def update_airport(request, airport_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    try:
        airport = Airport.objects.get(pk=airport_id)
    except (Airport.DoesNotExist, ValueError, ValidationError):
        raise Http404("Airport does not exist or invalid airport_id.")

    if request.method == "POST":
        form = AirportForm(request.POST, instance=airport)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("airports"))
    else:
        form = AirportForm(instance=airport)

    return render(request, "flights/update_airport.html", {
        "form": form,
        "airport": airport,
    })

def delete_airport(request, airport_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    try:
        airport = Airport.objects.get(pk=airport_id)
    except (Airport.DoesNotExist, ValueError, ValidationError):
        raise Http404("Airport does not exist or invalid airport_id.")  

    airport.delete()
    return HttpResponseRedirect(reverse("airports"))

def create_passenger(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("passengers"))
    else:
        form = PassengerForm()

    return render(request, "flights/create_passenger.html", {
        "form": form,
    })

def update_passenger(request, passenger_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    try:
        passenger = Passenger.objects.get(pk=passenger_id)
    except (Passenger.DoesNotExist, ValueError, ValidationError):
        raise Http404("Passenger does not exist or invalid passenger_id.")

    if request.method == "POST":
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("passengers"))
    else:
        form = PassengerForm(instance=passenger)

    return render(request, "flights/update_passenger.html", {
        "form": form,
        "passenger": passenger,
    })

def delete_passenger(request, passenger_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
    except (Passenger.DoesNotExist, ValueError, ValidationError):
        raise Http404("Passenger does not exist or invalid passenger_id.")  

    passenger.delete()
    return HttpResponseRedirect(reverse("passengers"))

def create_flight(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = FlightForm()

    return render(request, "flights/create_flight.html", {
        "form": form,
    })

def update_flight(request, flight_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    try:
        flight = Flight.objects.get(pk=flight_id)
    except (Flight.DoesNotExist, ValueError, ValidationError):
        raise Http404("Flight does not exist or invalid flight_id.")

    if request.method == "POST":
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = FlightForm(instance=flight)

    return render(request, "flights/update_flight.html", {
        "form": form,
        "flight": flight,
    })


def delete_flight(request, flight_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    try:
        flight = Flight.objects.get(pk=flight_id)
    except (Flight.DoesNotExist, ValueError, ValidationError):
        raise Http404("Flight does not exist or invalid flight_id.")  

    flight.delete()
    return HttpResponseRedirect(reverse("index"))