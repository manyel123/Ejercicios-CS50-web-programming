from django.urls import path

from . import views
# depending on the needs some functions from views can be called in htmls from urls
# also htmls such as "already_exists or not_found" for example, can be called directly in views functions
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.entry, name="entry"),
    path('search', views.search, name="search"),
    path('new_entry', views.new_entry, name="new_entry"),
    path('save_new_entry', views.save_new_entry, name="save_new_entry"),
    path('edit_entry', views.edit_entry, name="edit_entry"),
    path('save_edit', views.save_edit, name="save_edit"),
    path('random_entry', views.random_entry, name="random_entry"),
]