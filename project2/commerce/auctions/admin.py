from django.contrib import admin

from .models import Category, User, Listing, Watchlist, Comments, Bid


admin.site.register(Category)
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bid)