from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta
from .theme import Theme
from apps.base.models import BaseModel
from .theme import Theme


class Workshop(BaseModel):
    title = models.CharField(max_length=200)
    duration = models.DurationField(
        validators=[MinValueValidator(timedelta(minutes=1)), MaxValueValidator(timedelta(days=7))]
    )
    theme = models.ForeignKey(Theme, on_delete=models.RESTRICT)
    description = models.TextField()
    necessities = models.TextField()
    is_sensitive = models.BooleanField(default=False)

    # Related Many field
    # These are the related many fields that are opposites of ForeignKey or ManyToMany fields. We add them here in comment for documentation purposes
    #
    # building_blocks (BuildingBlockInstances)

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.building_blocks.all()) < 1:
            raise ValidationError("A workshop needs at least one building block")
