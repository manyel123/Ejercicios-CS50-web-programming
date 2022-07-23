from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("save", views.save_new_entry, name="save"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("edit_entry", views.edit_entry, name="edit_entry"),
    path("save_edit", views.save_edit, name="save_edit")
]