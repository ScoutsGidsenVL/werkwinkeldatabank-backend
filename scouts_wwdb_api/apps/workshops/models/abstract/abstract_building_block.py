from django.db import models
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.base.models import BaseModel
from ...models.category import Category


class AbstractBuildingBlock(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.DurationField(
        validators=[MinValueValidator(timedelta(minutes=1)), MaxValueValidator(timedelta(days=1))]
    )
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    short_description = models.CharField(max_length=500)

    class Meta:
        abstract = True
