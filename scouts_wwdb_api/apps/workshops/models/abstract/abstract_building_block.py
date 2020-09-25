from django.db import models
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.base.models import BaseModel
from ...models.category import Category
from ...models.theme import Theme


class AbstractBuildingBlock(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.DurationField(
        validators=[MinValueValidator(timedelta(minutes=1)), MaxValueValidator(timedelta(days=1))]
    )
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True)
    # Its django best practice to not set charfields nullable, an empty string will be used as empty field
    short_description = models.CharField(max_length=500, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.RESTRICT, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    buildingblock_necessities = models.TextField(blank=True, null=True)
    is_sensitive = models.BooleanField(default=False)

    class Meta:
        abstract = True
