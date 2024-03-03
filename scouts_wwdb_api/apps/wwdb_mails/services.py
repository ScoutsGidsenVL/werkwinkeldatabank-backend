from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .mails import mails


def send_wwdb_mail(*, subject: str, html_message: str, from_email: str = None, recipients: list = []):
    if not recipients:
        if not settings.DEFAULT_EMAIL_RECIPIENTS:
            raise ImproperlyConfigured("DEFAULT_EMAIL_RECIPIENTS setting is not set or empty")

        recipients = settings.DEFAULT_EMAIL_RECIPIENTS

    text_message = strip_tags(html_message)
    send_mail(subject, text_message, from_email, recipients, fail_silently=False, html_message=html_message)


def get_mail_subject_and_message(*, template: str, **kwargs):
    mail = mails.get(template)
    if not mail:
        raise Exception("Calling unknown mail template: %s" % template)

    return (mail.get("subject"), render_to_string(mail.get("template"), kwargs))


def send_template_mail(*, template: str, title: str = None, from_email: str = None, recipients: list = [], **kwargs):
    subject_message = get_mail_subject_and_message(template=template, **kwargs)

    send_wwdb_mail(
        subject=subject_message[0] + ": " + title,
        html_message=subject_message[1],
        from_email=from_email,
        recipients=recipients,
    )
