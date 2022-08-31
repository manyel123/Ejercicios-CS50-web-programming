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
from. models import Comments
from. models import Category

from .forms import ListingForm


# returns all listings from db
def get_all_listings():
    return Listing.objects.all()


# returns all watchlists form db
def get_all_watchlists():
    return Watchlist.objects.all()


# returns object id from POST
def get_listing_id(request):
    return request.POST["listing_id"]


# returns the whole object from POST
def get_listing_obj(request):
    return Listing.objects.get(id=request.POST.get('listing_id'))


# returns only active listings from db
def get_active_listings():
    return Listing.objects.filter(is_active=True)


# returns only inactive listings from db
def get_inactive_listings():
    return Listing.objects.filter(is_active=False)


# function to check if the listing viewed is being watched by the current user 
@login_required
def is_watched(request, pk):
    wl = get_all_watchlists()

    # get the listing to check if is watched or not
    obj_listing = Listing.objects.get(id=pk)

    # checks if the listing is watched by the current user or not
    for w in wl:
        if w.user_id == request.user and w.listing_id == obj_listing:
            return True
    return False


# returns the max bid information(amount, user) as a list
def get_max_bid(pk):
    obj_listing = Listing.objects.get(id=pk)
    bids = obj_listing.bid_listings.all()
    max_bid = 0
    max_user = User()
    for b in bids:
        if b.amount > max_bid:
            max_bid = b.amount
            max_user = b.user_id

    return max_bid, max_user


# function for counting the bids on each listing
def count_bids(pk):
    obj_listing = Listing.objects.get(id=pk)
    bids = obj_listing.bid_listings.all()
    bid_count = int(len(bids))
    return bid_count


# gets all the watchlists for a particular user
@login_required
def get_user_watchlist(request):
    wl = get_all_watchlists()
    user_wl = wl.objects.filter(user_id=request.user)
    return user_wl


""" This fuction will return all the listings being watched by the current user. """
@login_required
def display_watchlist(request):
    all_listings = get_all_listings()
    wl = get_all_watchlists()
    filtered_listings = []

    # filtering the listings being watched by the user
    for listing in all_listings:
        for w in wl:
            if w.user_id == request.user and w.listing_id == listing:
                filtered_listings.append(listing)

    # return the count and the listings to be displayed in the template
    return render(request, "auctions/watchlist.html", {
        'listings': filtered_listings,
        'count': len(filtered_listings)
    })


# send all inactive listings to the template to be displayed
def closed_listings(request):
    return render(request, "auctions/index.html", {
        'listings': get_inactive_listings(),
        'inactive': "display"
    })


# send all active listings to the template to be displayed
def index(request):
    return render(request, "auctions/index.html", {
        'listings': get_active_listings(),
        'active': "display"
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
        email    = request.POST["email"]

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


# create a new listing to be saved into db
@login_required
def create_listing(request):
    if request.method == "POST":

        # django form which gets the data for a new listing
        form = ListingForm(request.POST)

        # validates if initial bid is major to cero before saving it
        if float(request.POST.get('initial_bid')) <= 0:
            return render(request, "auctions/error.html", {
                "message": "Initial bid must be major to cero."
            })

        # validates form integrity and saves it into db    
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user_id = request.user
            listing.save()        

        # after saving a new listing it return to the index page   
            return HttpResponseRedirect(reverse("index"))
    else:
        # if the attempted method is different to post it returns the form info w/o saving it 
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            'form': form
        })


# returns a single listing given request and the id for the listing to display
def listing_detail(request, pk):

    # gets the listing given on the "pk" parameter
    if Listing.objects.filter(id=pk):

        """ Only if the listing exists the details and elements to be displayed
            are created. These are related below."""
        
        # getting all the comments for this particular listing
        listing_comments = Comments.objects.filter(listing_id=pk)

        # getting the max bid information which return as a list; pk is given as parameter
        max_bid_info     = get_max_bid(pk)
        # getting the max bid amount from the list
        max_bid          = max_bid_info[0]
        # getting the user with the max bid for this particular listing
        max_bid_user     = max_bid_info[1]

        # counting all the bids for a particular listing
        bid_count        = count_bids(pk)

        # getting current listing from the pk parameter
        current_listing  = Listing.objects.get(id=pk) 

        # if the current list exists and is active
        if current_listing.is_active == True:  

            """ to check if current user is the listing creator to be able to close the listing,
                if listing exist and current user is the creator of the listing he will be
                able to close it. The next situations are evaluated in this view: """

            """ If the current user is the creator"""

            if request.user == current_listing.user_id:

                # if listing exists and current user is the creator and the listing is watched by him
                """ If the listing is being watched by the creator the next paratemers
                    will be sent to the template, depending on the parameters sent, different
                    information will be displayed in the template. """
                if is_watched(request, pk) == True:

                    return render(request, "auctions/listing_detail.html", {
                        "listing"       : Listing.objects.get(id=pk),
                        "pk"            : pk,
                        "max_bid"       : max_bid,
                        "bid_count"     : bid_count,
                        "user_logedin"  : "True",
                        "is_creator"    : "True",
                        "message_iw"    : "is_watched",
                        "comments"      : listing_comments
                    })

                # if listing exists and current user is the creator and IS NOT watched by him
                elif is_watched(request, pk) == False:

                    return render(request, "auctions/listing_detail.html", {
                        "listing": Listing.objects.get(id=pk),
                        "pk": pk,
                        "max_bid": max_bid,
                        "bid_count": bid_count,
                        "user_logedin": "True",
                        "is_creator": "True",
                        "message_inw": "is_not_watched",
                        "comments": listing_comments
                    })

            """ if the current user has the highest bid for the listing """
            # if listing exist and current user has the highest bid
            if max_bid_user == request.user:
                # if listing exist and current user has the highest bid and is watched by him
                if is_watched(request, pk) == True:

                    return render(request, "auctions/listing_detail.html", {
                        "listing": Listing.objects.get(id=pk),
                        "pk": pk,
                        "max_bid": max_bid,
                        "bid_count": bid_count,
                        "max_bid_user": "is_max_bid_user",
                        "user_logedin": "True",
                        "message_iw": "is_watched",
                        "comments": listing_comments
                    })

                # if listing exist and current user has the highest bid and is NOT watched by him
                elif is_watched(request, pk) == False:

                    return render(request, "auctions/listing_detail.html", {
                        "listing": Listing.objects.get(id=pk),
                        "pk": pk,
                        "max_bid": max_bid,
                        "bid_count": bid_count,
                        "max_bid_user": "is_max_bid_user",
                        "user_logedin": "True",
                        "message_inw": "is_not_watched",
                        "comments": listing_comments
                    })

            else:
                """ if listing exist and current user HAS NOT the highest bid and is watched by him """
                if is_watched(request, pk) == True:

                    return render(request, "auctions/listing_detail.html", {
                        "listing": Listing.objects.get(id=pk),
                        "pk": pk,
                        "max_bid": max_bid,
                        "bid_count": bid_count,
                        "user_logedin": "True",
                        "message_iw": "is_watched",
                        "comments": listing_comments
                    })

                # if listing exist and current user HAS NOT the highest bid and is NOT watched by him
                elif is_watched(request, pk) == False:

                    return render(request, "auctions/listing_detail.html", {
                        "listing": Listing.objects.get(id=pk),
                        "pk": pk,
                        "max_bid": max_bid,
                        "bid_count": bid_count,
                        "user_logedin": "True",
                        "message_inw": "is_not_watched",
                        "comments": listing_comments
                    })

                # if listing exist and THERE IS NOT current user(is not logged in)
                else:
                    return render(request, "auctions/listing_detail.html", {
                        "listing": Listing.objects.get(id=pk),
                        "pk": pk,
                        "max_bid": max_bid,
                        "bid_count": bid_count,
                        "comments": listing_comments
                    })

        else:
            """ if the listing exist but IS NOT active. """
            # if the listing exist, IS NOT active, but the winner is seeing the listing
            if max_bid_user == request.user:

                return render(request, "auctions/listing_detail.html", {
                    "listing": Listing.objects.get(id=pk),
                    "pk": pk,
                    "max_bid": max_bid,
                    "bid_count": bid_count,
                    "max_bid_user": "is_max_bid_user",
                    "winner": "True",
                    "active": "False",
                    "comments": listing_comments
                })

            # if the listing exist, IS NOT active, and the current user is not the winner
            return render(request, "auctions/listing_detail.html", {
                "listing": Listing.objects.get(id=pk),
                "pk": pk,
                "max_bid": max_bid,
                "bid_count": bid_count,
                "active": "False",
                "comments": listing_comments
            })

    # if listing in pk DOES NOT exist
    else:
        return render(request, "auctions/error.html", {
            "message": "The listing does not exist."
        })


""" Function for adding a listing into the watchlist through the "watchlist" button,
    this record will be saved into the db. """
@login_required
def add_to_watchlist(request):
    if request.method == "POST":

        id_listing = get_listing_id(request)
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


""" Function for deleting a watchlist from the db. """
@login_required
def del_watchlist(request):
    if request.method == "POST":

        id_listing = get_listing_id(request)
        obj_listing = get_listing_obj(request)
        wl = get_all_watchlists()

        for w in wl:
            if w.user_id == request.user and w.listing_id == obj_listing:
                query = Watchlist.objects.get(pk=w.id)
                query.delete()
        return listing_detail(request, id_listing)

    else:
        return render(request, "auctions/index.html")


""" Funcion for saving a new bid into the db. """
@login_required
def new_bid(request):
    if request.method == "POST":

        user_id = request.user
        id_listing = get_listing_id(request)
        obj_listing = get_listing_obj(request)
        bid_amount = request.POST['bid_amount']
        bids = obj_listing.bid_listings.all()
        max_bid = 0
        init_bid = obj_listing.initial_bid

        # gets the amount of the max bid
        for b in bids:
            if b.amount > max_bid:
                max_bid = b.amount

        # evaluates if the posted bid is major to the current and the initial bid, if is not:
        if float(bid_amount) < max_bid or float(bid_amount) < init_bid:
            return render(request, "auctions/error.html", {
                "message": "Error. Your bid must be major to current and initial bid."
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


""" Function for closing a listing, it makes use of the "close listing button". """
# this button will only be displayed to the user who created the listing
@login_required
def close_listing(request):
    if request.method == "POST":
        Listing.objects.filter(id=request.POST.get('listing_id')).update(is_active=False)
        return HttpResponseRedirect(reverse("index"))


""" This function will save a new comment in a particular listing. """
@login_required
def new_comment(request):
    if request.method == "POST":

        user_id = request.user
        id_listing = get_listing_id(request)
        obj_listing = get_listing_obj(request)
        comment = request.POST['comment']
        
        try:
            comment = Comments.objects.create(user_id=user_id.id, listing_id=obj_listing.id, comment=comment)
            comment.save()
            
        except IntegrityError:
            return render(request, "auctions/error.html", {
                "message": "Error while saving your comment."
            })
        return listing_detail(request, id_listing)

    else:
        return render(request, "auctions/index.html")


""" This function will return all the categories to be displayed in the template as links. """
def display_categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': categories
    })


""" This funcion will return the listings from a single category to be displayed as a list. """
def display_category(request,pk):
    all_listings = get_all_listings()
    category = Category.objects.get(id=pk)
    filtered_listings = []

    for listing in all_listings:
        if listing.category_id == category:
            filtered_listings.append(listing)

    return render(request, "auctions/category.html", {
        'category': category,
        'pk': pk,
        "listings": filtered_listings
    })