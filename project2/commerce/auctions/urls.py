from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:pk>", views.listing_detail, name="listing_detail"),
    path("watchlist_add", views.add_to_watchlist, name="watchlist_add"),
    path("watchlist_del", views.del_watchlist, name="watchlist_del"),
    path("new_bid", views.new_bid, name="new_bid"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
]
