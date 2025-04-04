from django.contrib import admin

from .models import Maintenance, Periodic

admin.site.register([Maintenance, Periodic])
