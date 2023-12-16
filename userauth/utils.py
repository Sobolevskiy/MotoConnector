from django.core.mail import send_mail


def send_sync_verification_email(email, code):
    send_mail(
        "Код подтверждения",
        f"Ваш код потверждения {code}",
        None,
        [email],
        fail_silently=False,
    )