from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from . models import Flight, Passenger
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
#    return HttpResponse("Flights")
#    if not request.user.is_authenticated:
#        return render(request, "users/login.html", {"message": "None"})
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight doesn't exist. ")

    context = {
     "flight": flight,
     "passengers": flight.passengers.all(),
     "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)


def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "No selection"})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No passengers"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No such flight"})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid Credentials"})


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged Out"})
