from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):
    # checking if user is authenticated from request
    if not request.user.is_authenticated:
        # if user is not authenticated, will be redirect to login url
        return HttpResponseRedirect(reverse("login"))
        # if user is authenticated, will be redirect to user template
    return render(request, "users/user.html")


# function for login, it makes use of authenticate and login imports
def login_view(request):
    # login information is given by a post method in the login template form
    if request.method == "POST":
        # creating an username with post username info
        username = request.POST["username"]
        # creatomg a password with post password info
        password = request.POST["password"]

        # tries to authenticate a user and save it into user variable if the authentication is successful
        user = authenticate(request, username=username, password=password)

        # if user different to None it means the user was authenticated
        if user is not None:
            # then the user is loged in with user object
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # if user is None, means that the credential are not valid so nothing was saved into the user object
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "users/login.html ")


# function for login out, it makes use of the logout import
def logout_view(request):
    # logs out the user
    logout(request)

    # return the login page with a log out message
    return render(request, "users/login.html", {
        "message": "Logged out."
    })