from django.db import models
from apps.base.models import BaseModel, DisabledFieldModelMixin
from ..managers import ThemeManager


class Theme(DisabledFieldModelMixin, BaseModel):
    # Overwrite manager
    objects = ThemeManager()

    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
