"""apps.workshops.models.theme."""

from django.db import models

from apps.base.models import BaseModel, DisabledFieldModelMixin
from apps.workshops.managers import ThemeManager


class Theme(DisabledFieldModelMixin, BaseModel):
    objects = ThemeManager()  # Overwrite manager
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Related Many field
    # workshops (Workshop)

    def __str__(self):
        return str(self.title)
