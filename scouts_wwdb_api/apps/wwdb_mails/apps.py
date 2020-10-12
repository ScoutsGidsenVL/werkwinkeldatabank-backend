from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MailConfig(AppConfig):
    name = "apps.wwdb_mails"
