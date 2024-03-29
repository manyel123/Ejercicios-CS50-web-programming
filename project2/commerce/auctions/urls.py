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
    path("new_comment", views.new_comment, name="new_comment"),
    path("display_watchlist", views.display_watchlist, name="display_watchlist"),
    path("display_categories", views.display_categories, name="display_categories"),
    path("category/<int:pk>", views.display_category, name="display_category"),
    path("category/listing/<int:pk>", views.listing_detail, name="listing_detail"),
]
