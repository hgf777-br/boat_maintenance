from django.contrib import admin

from .models import Occurrence, Item, CheckInOut, CheckInOutItem

admin.site.register(Occurrence)
admin.site.register(Item)
admin.site.register(CheckInOut)
admin.site.register(CheckInOutItem)
