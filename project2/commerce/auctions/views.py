from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .models import Listing
from .models import Watchlist
from .forms import ListingForm


def get_all_listings():
    return Listing.objects.all


def get_listing_by_id(id):
    return Listing.objects.filter(id=id)


def get_active_listings():
    return Listing.objects.filter(is_active=True)


def index(request):
    active_listings = get_all_listings()
    return render(request, "auctions/index.html", {
        'listings': active_listings
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


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if float(request.POST.get('initial_bid')) <= 0:
            return render(request, "auctions/error.html", {
                "message": "Initial bid must be major to cero."
            })
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user_id = request.user
            listing.save()        
        # Necesita retornar la vista del artículo    
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        'form': form
    })

    
def listing_detail(request, pk):
    if Listing.objects.filter(id=pk):
        return render(request, "auctions/listing_detail.html", {
            "listing": Listing.objects.get(id=pk),
            "pk": pk
        })
    else:
        return render(request, "auctions/error.html", {
            "message": "The listing does not exist."
        })
        
@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        user_id = request.user
        listing_id = request.POST["listing_id"]
        watched = True
        try:
            user = Watchlist.objects.create(user_id=user_id, listing_id=Listing(listing_id), watched=watched)
            user.save()
        except IntegrityError:
            return render(request, "auctions/error.html", {
                "message": "Uknown error."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/index.html")
        #return Watchlist.objects.create(
            #user_id=request.user, 
            #listing_id = listing,
            #listing_id=Listing.objects.filter(id=request.POST.get('listing_id'))[0],
            #listing_id=Listing.objects.get(id=request.POST.get('listing_id')), 
            #watched=True)
