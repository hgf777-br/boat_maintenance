from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# from occurrence.models import Item


class Boat(models.Model):
    YEAR_CHOICES = [(r, r) for r in range(1970, datetime.today().year + 1)]

    class Manufacturer(models.TextChoices):
        FAST = 'Fast', 'Fast'
        DELTA = 'Delta', 'Delta'
        BENETEAU = 'Beneteau', 'Beneteau'
        JENNEAU = 'Jenneau', 'Jenneau'
        MJ = 'MJ', 'MJ'

    name = models.CharField(max_length=64, unique=True, verbose_name=_('name'))
    number_shares = models.PositiveIntegerField(default=8, verbose_name=_('number of shares'))
    manufacturer = models.CharField(max_length=64, choices=Manufacturer, default=Manufacturer.FAST,
                                    verbose_name=_('manufacturer'))
    model = models.CharField(max_length=64, blank=True, null=True)
    year_built = models.PositiveIntegerField(choices=YEAR_CHOICES, default=1970)
    items = models.ManyToManyField("occurrence.Item", through="BoatItem", verbose_name=_('items'))
    users_for_reminders = (
        models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserReminder", verbose_name=_('users for reminders'))
    )
    share_owner_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_1',
                                      on_delete=models.SET_NULL, blank=True, null=True,)
    share_owner_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_2',
                                      on_delete=models.SET_NULL, blank=True, null=True,)
    share_owner_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_3',
                                      on_delete=models.SET_NULL, blank=True, null=True,)
    share_owner_4 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_4',
                                      on_delete=models.SET_NULL, blank=True, null=True,)
    share_owner_5 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_5',
                                      on_delete=models.SET_NULL, blank=True, null=True)
    share_owner_6 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_6',
                                      on_delete=models.SET_NULL, blank=True, null=True)
    share_owner_7 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_7',
                                      on_delete=models.SET_NULL, blank=True, null=True)
    share_owner_8 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='share_owner_8',
                                      on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.name

    def get_owners(self, id=False):
        SHARE_OWNERS = [
            self.share_owner_1,
            self.share_owner_2,
            self.share_owner_3,
            self.share_owner_4,
            self.share_owner_5,
            self.share_owner_6,
            self.share_owner_7,
            self.share_owner_8,
        ]
        response = []
        for idx in range(self.number_shares):
            response.append(SHARE_OWNERS[idx].id if SHARE_OWNERS[idx] and id else SHARE_OWNERS[idx])
        return response

    def set_owners(self, owners):
        user_model = get_user_model()
        other_boats = Boat.objects.exclude(pk=self.pk)
        self.share_owner_1 = self._set_new_owner(owners[0], user_model, other_boats)
        self.share_owner_2 = self._set_new_owner(owners[1], user_model, other_boats)
        self.share_owner_3 = self._set_new_owner(owners[2], user_model, other_boats)
        self.share_owner_4 = self._set_new_owner(owners[3], user_model, other_boats)
        if self.number_shares > 4:
            self.share_owner_5 = self._set_new_owner(owners[4], user_model, other_boats)
        if self.number_shares > 5:
            self.share_owner_6 = self._set_new_owner(owners[5], user_model, other_boats)
        if self.number_shares > 6:
            self.share_owner_7 = self._set_new_owner(owners[6], user_model, other_boats)
        if self.number_shares > 7:
            self.share_owner_8 = self._set_new_owner(owners[7], user_model, other_boats)
        self.save()

    def _set_new_owner(self, new_owner, user_model, other_boats):
        if new_owner != '0':
            new_owner = user_model.objects.get(pk=new_owner)
            if self._new_owner_has_boat(new_owner, other_boats):
                raise ValueError(f"O proprietário <strong>{new_owner.get_full_name()}</strong> já possui um barco")
            else:
                return new_owner
        return None

    def _new_owner_has_boat(self, new_owner, other_boats):
        for boat in other_boats:
            if new_owner in boat.get_owners():
                return True
        return False


class BoatItem(models.Model):
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, related_name='boat_items')
    item = models.ForeignKey("occurrence.Item", on_delete=models.CASCADE, related_name='boat_items')

    def __str__(self):
        return f"{self.boat.name} <> {self.item.name}"


class UserReminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user"))
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, verbose_name=_("boat"))

    def __str__(self):
        return f"{self.user.get_full_name()} <> {self.boat.name}"
