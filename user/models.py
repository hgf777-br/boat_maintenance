from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.http import JsonResponse
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
        subject = "Nova senha para o sistema NGO"
        message = f"""
        Olá {self.first_name},

        Foi solicitada uma nova senha para o seu usuário.
        Segue abaixo a senha gerada para seu acesso ao sistema:

        usuário: {self.username}
        senha provisória: {new_password}

        Por favor faça o login no sistema abaixo

        {current_site}

        usando seu usuário, ou o seu email, e a senha enviada.

        Pedimos que altere a senha para uma pessoal de sua escolha assim que possível.

        Henrique Faria
        """
        self.email_user(subject, message, settings.SYSTEM_EMAIL)
        
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
    