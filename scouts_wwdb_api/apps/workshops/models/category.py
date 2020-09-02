from django.db import models
from apps.base.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title
