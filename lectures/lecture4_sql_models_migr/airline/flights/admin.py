from django.contrib import admin

from .models import Flight, Airport, Passenger

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    # elements to be displayed in django admin interface for flights
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    # adds an horizontal filter for passenger flights into passengers admin page
    filter_horizontal = ("flights",)

admin.site.register(Airport)
# tells django to use FlighAdmin for Flight, in django admin interface
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)