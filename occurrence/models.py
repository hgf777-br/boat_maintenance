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
    engine_hours = models.PositiveIntegerField(verbose_name=_("engine hours"), blank=True, null=True)
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


class Checkout(models.Model):
    date = models.DateField(verbose_name=_("date"))
    engine_hours = models.PositiveIntegerField(verbose_name=_("engine hours"), blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("creator"))
    boat = models.ForeignKey("boat.Boat", on_delete=models.PROTECT, verbose_name=_("boat"))
    obs = models.TextField(verbose_name=_("observation"), blank=True)
    items = models.ManyToManyField(Item, through="CheckoutItem", verbose_name=_("items"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return f"Checkout {self.boat} {self.creator} {self.date}"


class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, verbose_name=_("checkout"))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_("item"))
    is_ok = models.BooleanField(default=True, verbose_name=_("is ok"))
    obs = models.TextField(verbose_name=_("observation"), blank=True)

    def __str__(self):
        return f"{self.checkout} <> {self.item}"
