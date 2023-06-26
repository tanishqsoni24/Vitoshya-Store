from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import format_html


def send_account_activation_email(email, email_token):
    subject = "Account Activation Email"
    email_from = settings.EMAIL_HOST_USER
    activation_link = f"http://127.0.0.1:8000/accounts/activate/{email_token}"
    message = format_html(
        f"Hi {email},<br>"
        f"Please click on the button below to activate your account:<br>"
        f'<a href="{activation_link}" style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">Click Here</a>'
    )
    send_mail(subject,'', email_from, [email], html_message=message)