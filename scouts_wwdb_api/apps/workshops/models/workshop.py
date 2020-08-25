from django.db import models
from .theme import Theme
from apps.base.models import BaseModel
from .theme import Theme


class Workshop(BaseModel):
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    theme = models.ForeignKey(Theme, on_delete=models.RESTRICT)
    description = models.TextField()
    necessities = models.TextField()

    def __str__(self):
        return self.title
