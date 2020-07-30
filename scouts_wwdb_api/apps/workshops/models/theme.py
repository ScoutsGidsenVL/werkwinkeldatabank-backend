from django.db import models
from apps.base.models import BaseModel


class Theme(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title