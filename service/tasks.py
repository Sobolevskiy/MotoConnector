from django.core.mail import send_mail

from MotoConnector.celery import app


@app.task(name='send_verification_email')
def send_verification_email(email, code):
    send_mail(
        "Код подтверждения",
        f"Ваш код потверждения {code}",
        None,
        [email],
        fail_silently=False,
    )
