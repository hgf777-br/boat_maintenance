from django.contrib import admin

from.models import Occurrence, Item, Checkout, CheckoutItem

admin.site.register(Occurrence)
admin.site.register(Item)
admin.site.register(Checkout)
admin.site.register(CheckoutItem)
