from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models

from maintenance.models import Sectors, Maintenance


class Occurrence(models.Model):
    description = models.CharField(max_length=256, verbose_name=_("description"))
    date = models.DateField(verbose_name=_("date"))
    sector = models.CharField(
        max_length=2, choices=Sectors, verbose_name=_("sector"), blank=False, default=Sectors.ENGINE
        )
    obs = models.TextField(verbose_name=_("observation"), blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("creator"))
    boat = models.ForeignKey("boat.Boat", on_delete=models.PROTECT, verbose_name=_("boat"))
    hour_meter = models.PositiveIntegerField(verbose_name=_("hour meter"), blank=True, null=True)
    maintenance = models.ForeignKey(
        Maintenance, on_delete=models.PROTECT, verbose_name=_("maintenance"), blank=True, null=True
        )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.description


class Item(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("name"))
    sector = models.CharField(max_length=2, choices=Sectors, verbose_name=_("sector"),
                              blank=False, default=Sectors.ENGINE)

    def __str__(self):
        return self.name


class CheckInOut(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("creator"))
    boat = models.ForeignKey("boat.Boat", on_delete=models.PROTECT, verbose_name=_("boat"))
    checkin_date = models.DateField(verbose_name=_("date"))
    checkin_hour_meter = models.PositiveIntegerField(verbose_name=_("hour meter"))
    checkin_obs = models.TextField(verbose_name=_("observation"), blank=True)
    checkout_date = models.DateField(verbose_name=_("date"), blank=True, null=True)
    checkout_hour_meter = models.PositiveIntegerField(verbose_name=_("hour meter"), blank=True, null=True)
    checkout_obs = models.TextField(verbose_name=_("observation"), blank=True)
    checkout_items = models.ManyToManyField(Item, through="CheckInOutItem", verbose_name=_("items"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return f"CheckInOut {self.boat} {self.creator} {self.checkin_date} {self.checkout_date}"


class CheckInOutItem(models.Model):
    checkout = models.ForeignKey(CheckInOut, on_delete=models.CASCADE, verbose_name=_("checkout"))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_("item"))
    is_ok = models.BooleanField(default=True, verbose_name=_("is ok"))
    obs = models.TextField(verbose_name=_("observation"), blank=True)

    def __str__(self):
        return f"{self.checkout} <> {self.item}"
