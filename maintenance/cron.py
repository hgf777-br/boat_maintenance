from django.core.mail import send_mail

from boat.models import Boat
from maintenance.models import Maintenance


def send_email_for_maintenances():
    print('Sending email for pending maintenance...')
    boat = Boat.objects.get(name='Blue Note')
    pending_maintenances = Maintenance.objects.filter(boat=boat, completed=False)
    message = ''
    for maintenance in pending_maintenances:
        message += f"Manutenção: {maintenance.description}\n"
        message += f"Data: {maintenance.date}\n"
        message += f"Técnico: {maintenance.technician.name}\n\n"
    send_mail(
        "Teste de email de manutenção",
        message,
        "mandaprohgf@gmail.com",
        ["hgf777@gmail.com"],
        fail_silently=False,
    )
