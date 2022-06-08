from django.core.mail import send_mail
from django.conf import settings

def send_forgot_password_mail(email, token):
    try:
        subject = "Your forget password link"
        message = f"Please click the following link to reset your password http://127.0.0.1:8000/change-password/{token}/"
        email_form = settings.EMAIL_HOST_USER
        recipient_list = ['email']
        send_mail(subject, message, email_form, recipient_list)

        return True
    except Exception as e:
        return e