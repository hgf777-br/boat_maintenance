from django.db import models
from django.utils.translation import gettext_lazy as _


class Technician(models.Model):
    class Specialities(models.TextChoices):
        MECHANIC = 'ME', _('mechanic')
        PLUMBER = 'PL', _('plumber')
        ELETRICIAN = 'EL', _('electrician')
        CARPENTER = 'CA', _('carpenter')
        PAINTER = 'PA', _('painter')
        UPHOLSTERER = 'UP', _('upholsterer')
        ENGINEER = 'EN', _('engineer')
        OTHER = 'OT', _('other')

    name = models.CharField(max_length=64, verbose_name=_("name"))
    phone = models.CharField(max_length=16, verbose_name=_("cell phone"))
    email = models.EmailField(max_length=256, verbose_name=_("email"))
    speciality = models.CharField(max_length=2, choices=Specialities, verbose_name=_("speciality"),
                                  blank=False, default=Specialities.MECHANIC,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.name
