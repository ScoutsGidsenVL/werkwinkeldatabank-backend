"""apps.admin."""
from django.contrib import admin
from models import Theme, Workshop

admin.site.register(Workshop)
admin.site.register(Theme)
