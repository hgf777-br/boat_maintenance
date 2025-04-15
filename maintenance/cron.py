from django.core.mail import send_mail


def send_email_for_maintenances():
    print('Sending email for pending maintenance...')
    send_mail(
        "Teste de email de manutenção",
        "Aqui vão as manutenções pendentes.",
        "mandaprohgf@gmail.com",
        ["hgf777@gmail.com"],
        fail_silently=False,
    )
