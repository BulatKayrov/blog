from django.conf import settings
from django.core.mail import send_mail


def verified_accounts(email, uuid_code):
    host = 'http://127.0.0.1:8000/users/verify/'
    send_mail(
        "Subject here",
        f"Для подтверждения регистрации перейдите по ссылке {host}{uuid_code}/",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )



