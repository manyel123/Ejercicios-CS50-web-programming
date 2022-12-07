from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        # return all flights
        "flights": Flight.objects.all()
    })

# function to render a particular flight
def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        # flight to be rendered
        "flight": flight,
        # passengers who will go into the flight
        "passengers": flight.passengers.all(),
        # passengers that are not in the current flight(used for book to add new passengers into a flight)
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

# function to add passengers into a flight from flight.html
def book(request, flight_id):
    if request.method == "POST":
        # gets the current flight
        flight = Flight.objects.get(pk=flight_id)
        # gets the passenger to be included into the flight from template's form
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        # adds or register the passenger into the flight
        passenger.flights.add(flight)

        # reverse to flight page with the argument flight.id which is the flight to be render
        # args=(flight.id,) should have a comma because is structured as a tuple
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))