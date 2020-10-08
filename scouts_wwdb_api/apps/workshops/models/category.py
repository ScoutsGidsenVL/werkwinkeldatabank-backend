from django.db import models
from apps.base.models import BaseModel, DisabledFieldModelMixin
from ..managers import CategoryManager


class Category(DisabledFieldModelMixin, BaseModel):
    # Overwrite manager
    objects = CategoryManager()

    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title
