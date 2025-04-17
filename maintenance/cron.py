from django.core.mail import send_mail

from boat.models import Boat
from maintenance.models import Maintenance


def send_email_for_maintenances():
    print('Sending email for pending maintenance...')
    boat = Boat.objects.get(name='Blue Note')
    pending_maintenances = Maintenance.objects.filter(boat=boat, completed=False).order_by('due_date')
    message = f'Veleiro {boat.name} -  manutenções pendentes:\n\n'
    for maintenance in pending_maintenances:
        message += f"manutenção: {maintenance.description}\n"
        message += f"data limite: {maintenance.due_date.strftime(r'%d/%m/%Y')}\n"
        message += f"setor: {maintenance.get_sector_display()}\n"
        if maintenance.schedule_date:
            message += f"data agendada: {maintenance.schedule_date.strftime(r'%d/%m/%Y')}\n"
            message += f"técnico: {maintenance.technician.name} - {maintenance.technician.phone}\n"
        message += f"{'-' * 80}\n\n"

    send_mail(
        "Teste de email de manutenção - IGNORAR vai  receber a cada 3 horas",
        message,
        "mandaprohgf@gmail.com",
        ["hgf777@gmail.com", "abelmferreira@gmail.com", "daniela@flipboatclub.com.br"],
        fail_silently=False,
    )
