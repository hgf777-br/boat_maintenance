from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from boat.models import Boat
from technician.models import Technician


class Sectors(models.TextChoices):
        ENGINE = 'EN', _('engine')
        HYCRAULIC = 'HY', _('hydraulic')
        ELETRIC = 'EL', _('electric')
        EQUIPMENT = 'EQ', _('equipment')
        CABLES = 'CA', _('cables')
        RIGGING = 'RI', _('rigging')
        OTHER = 'OT', _('other')


class Periodicity(models.TextChoices):
        WEEKLY = 'WE', _('weekly')
        BIWEEKLY = 'BW', _('bi-weekly')
        MONTHLY = 'MO', _('monthly')
        QUARTERLY = 'QU', _('quarterly')
        SEMI_ANNUALLY = 'SA', _('semi-annually')
        ANNUALLY = 'AN', _('annually')


class Maintenance(models.Model):
    
    description = models.CharField(max_length=256, verbose_name=_("description"))
    due_date = models.DateField(verbose_name=_("due date"))
    sector = models.CharField(max_length=2, choices=Sectors, verbose_name=_("sector"), blank=False, default=Sectors.ENGINE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("creator"))
    boat = models.ForeignKey(Boat, on_delete=models.PROTECT, verbose_name=_("boat"))
    schedule_date = models.DateField(verbose_name=_("schedule date"), blank=True, null=True)
    technician = models.ForeignKey(Technician, on_delete=models.PROTECT, verbose_name=_("technician"), blank=True, null=True)
    observation = models.TextField(verbose_name=_("observation"), blank=True)
    finish_date = models.DateField(blank=True, null=True, verbose_name=_("finish date"))
    completed = models.BooleanField(default=False, verbose_name=_("completed"))
    engine_hours = models.PositiveIntegerField(verbose_name=_("engine hours"), blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("value"), blank=True, null=True)
    periodic = models.ForeignKey("Periodic", on_delete=models.CASCADE, verbose_name=_("periodic"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.description
    
    def has_schedule_date(self):
        return self.schedule_date is not None
    
class Periodic(models.Model):
    DAY_CHOICES = [(r,r) for r in range(1,32)]
    WEEK_DAY = [_('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'), _('Friday'), _('Saturday'), _('Sunday')]
    MONTH_CHOICES = [_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), 
                    _('July'), _('August'), _('September'), _('October'), _('November'), _('December')]

    description = models.CharField(max_length=64, verbose_name=_("description"))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("creator"))
    boat = models.ForeignKey(Boat, on_delete=models.PROTECT, verbose_name=_("boat"))
    sector = models.CharField(max_length=2, choices=Sectors, verbose_name=_("sector"), blank=False, default=Sectors.ENGINE)
    periodicity = models.CharField(max_length=2, choices=Periodicity, default=Periodicity.MONTHLY, verbose_name=_("periodicity"))
    periodicity_day = models.PositiveIntegerField(choices=DAY_CHOICES, verbose_name=_("day of month"), blank=True, null=True)
    periodicity_month = models.PositiveIntegerField(choices=[(i, m) for i, m in enumerate(MONTH_CHOICES, 1)], verbose_name=_("month"), blank=True, null=True)
    periodicity_week_day = models.PositiveIntegerField(choices=[(i, d) for i, d in enumerate(WEEK_DAY, 1)], verbose_name=_("day of week"), blank=True, null=True)
    periodicity_value = models.PositiveIntegerField(verbose_name=_("periodicity value"), blank=True, null=True)
    last_run_date = models.DateField(verbose_name=_("last run date"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.description
    
    def new_due_date(self, base_date=datetime.today(), initial_run=False):
        month = base_date.month
        year = base_date.year
        match self.periodicity:
            case 'MO':
                if base_date.day >= self.periodicity_day or not initial_run:
                    month = month + 1 if month < 12 else 1
                due_date = datetime(year, month, self.periodicity_day)
            case 'WE'|'BW':
                if initial_run:
                    weekday_number = self.periodicity_week_day - 1
                    if base_date.weekday() >= weekday_number:
                        day_difference = 7 - abs(base_date.weekday() - weekday_number)
                    else:
                        day_difference = self.periodicity_week_day - base_date.weekday() - 1
                    due_date = base_date + timedelta(days=day_difference)
                    if self.periodicity == 'BW':
                        due_date += timedelta(days=7)
                else:
                    increase = 7 if self.periodicity == 'WE' else 14
                    due_date = base_date + timedelta(days=increase)
            case 'QU'|'SA'|'AN':
                    if initial_run:
                        if month >= self.periodicity_month:
                            year += 1
                        due_date = datetime(year, self.periodicity_month, self.periodicity_day)
                    else:
                        months = {'QU': 3, 'SA': 6, 'AN': 12}
                        month += months[self.periodicity]
                        if month > 12:
                            month -= 12
                            year += 1
                        due_date = datetime(year, month, self.periodicity_day)
        
        return due_date