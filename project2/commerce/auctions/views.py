from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .models import Listing
from .models import Watchlist
from .models import Bid
from .forms import ListingForm


def get_all_listings():
    return Listing.objects.all()


def get_all_watchlists():
    return Watchlist.objects.all()


# returns object id
def get_listing_id(request):
    return request.POST["listing_id"]


# returns the whole object
def get_listing_obj(request):
    return Listing.objects.get(id=request.POST.get('listing_id'))


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
    max_bid = get_max_bid(pk)
    bid_count = count_bids(pk)
    if Listing.objects.filter(id=pk):
        if is_watched(request, pk):
            return render(request, "auctions/listing_detail.html", {
                "listing": Listing.objects.get(id=pk),
                "pk": pk,
                "max_bid": max_bid,
                "bid_count": bid_count,
                "message_iw": "is_watched"
            })
        else:
            return render(request, "auctions/listing_detail.html", {
                "listing": Listing.objects.get(id=pk),
                "pk": pk,
                "max_bid": max_bid,
                "bid_count": bid_count,
                "message_inw": "is_not_watched"
            })
    else:
        return render(request, "auctions/error.html", {
            "message": "The listing does not exist."
        })


@login_required
def is_watched(request, pk):
    wl = get_all_watchlists()
    obj_listing = Listing.objects.get(id=pk)
    for w in wl:
        if w.user_id == request.user and w.listing_id == obj_listing:
            return True


def get_max_bid(pk):
    obj_listing = Listing.objects.get(id=pk)
    bids = obj_listing.bid_listings.all()
    max_bid = 0
    for b in bids:
        if b.amount > max_bid:
            max_bid = b.amount
    return max_bid


def count_bids(pk):
    obj_listing = Listing.objects.get(id=pk)
    bids = obj_listing.bid_listings.all()
    bid_count = int(len(bids))
    return bid_count


@login_required
def add_to_watchlist(request):
    id_listing = get_listing_id(request)
    if request.method == "POST":
        user_id = request.user
        listing_id = id_listing
        try:
            user = Watchlist.objects.create(user_id=user_id, listing_id=Listing(listing_id))
            user.save()
        except IntegrityError:
            return render(request, "auctions/error.html", {
                "message": "Error while adding to your watchlist."
            })
        return listing_detail(request, listing_id)
    else:
        return render(request, "auctions/index.html")


@login_required
def del_watchlist(request):
    id_listing = get_listing_id(request)
    obj_listing = get_listing_obj(request)
    if request.method == "POST":
        wl = get_all_watchlists()
        for w in wl:
            if w.user_id == request.user and w.listing_id == obj_listing:
                query = Watchlist.objects.get(pk=w.id)
                query.delete()
        return listing_detail(request, id_listing)
    else:
        return render(request, "auctions/index.html")


@login_required
def new_bid(request):
    user_id = request.user
    id_listing = get_listing_id(request)
    obj_listing = get_listing_obj(request)
    bid_amount = request.POST['bid_amount']
    bids = obj_listing.bid_listings.all()
    max_bid = 0
    init_bid = obj_listing.initial_bid
    if request.method == "POST":
        for b in bids:
            if b.amount > max_bid:
                max_bid = b.amount
        if float(bid_amount) < max_bid or float(bid_amount) < init_bid:
            return render(request, "auctions/error.html", {
                "message": "Error. Your bid must be major to current bid."
            })
        try:
            bid = Bid.objects.create(user_id=user_id,listing_id=obj_listing, amount=bid_amount)
            bid.save()
        except IntegrityError:
            return render(request, "auctions/error.html", {
                "message": "Error while saving your bid."
            })
        return listing_detail(request, id_listing)
    else:
        return render(request, "auctions/index.html")