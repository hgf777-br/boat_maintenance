from pathlib import Path
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from boat.models import Boat

from .utils import make_random_password
from .managers import CustomUserManager


class User(AbstractUser):
    class Profiles(models.TextChoices):
        SHARE_OWNER = "SO", _("share owner")
        OPERATOR = "OP", _("operator")
        MASTER = "MS", _("master")
        
    class Themes(models.TextChoices):
        AUTO = "AT", "auto"
        LIGHT = "LT", "light"
        DARK = "DK", "dark"

    profile = models.CharField(
        max_length=2,
        choices=Profiles.choices,
        default=Profiles.SHARE_OWNER,
        verbose_name=_("profile"),
    )
    theme = models.CharField(
        max_length=2,
        choices=Themes.choices,
        default=Themes.AUTO,
        verbose_name=_("theme"),
    )
    phone = models.CharField(max_length=16, verbose_name=_("cell phone"))
    email = models.EmailField(_("email address"), blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def send_new_password_email(self, request) -> None:
        # Send email with new password to user
        new_password = make_random_password()
        current_site = request.build_absolute_uri("/")[:-1]
        self.set_password(new_password)
        self.save()
        context = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "new_password": new_password,
            "current_site": current_site,
        }
        subject = "Nova senha para o sistema manuteção de embarcações"
        html_message = render_to_string("email/new_user_password.html", context)
        plain_message = strip_tags(html_message)
        self.email_user(subject, plain_message, settings.SYSTEM_EMAIL, html_message=html_message)
        
    def get_boat(self):
        boats = Boat.objects.all()
        for boat in boats:
            if (boat.share_owner_1 == self 
                or boat.share_owner_2 == self 
                or boat.share_owner_3 == self 
                or boat.share_owner_4 == self 
                or boat.share_owner_5 == self
                or boat.share_owner_6 == self
                or boat.share_owner_7 == self
                or boat.share_owner_8 == self
            ):
                return boat
            else:
                return None
        
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(upload_to="profiles/", blank=True)
    address = models.CharField(max_length=256, verbose_name=_("address"), blank=True)
    state = models.CharField(max_length=64, verbose_name=_("state"), blank=True)
    city = models.CharField(max_length=64, verbose_name=_("city"), blank=True)
    country = models.CharField(max_length=64, verbose_name=_("country"), blank=True)
    zip_code = models.CharField(max_length=16, verbose_name=_("zip code"), blank=True)
    birth_date = models.DateField(blank=True, verbose_name=_("birth date"), null=True)
    