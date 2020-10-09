from django.db import models
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from apps.base.models import BaseModel, DisabledFieldModelMixin
from .enums.building_block_type import BuildingBlockType
from .category import Category
from .theme import Theme
from ..managers import BuildingBlockTemplateManager


# This model represents a template for a building block that can be used by scouts admins to manage some predefined templates
# These are not actual building blocks and cant be connected directly to a workshop
class BuildingBlockTemplate(DisabledFieldModelMixin, BaseModel):
    # Overwrite manager
    objects = BuildingBlockTemplateManager()

    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.DurationField(
        validators=[MinValueValidator(timedelta(minutes=1)), MaxValueValidator(timedelta(days=1))]
    )
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True)
    # Its django best practice to not set charfields nullable, an empty string will be used as empty field
    short_description = models.CharField(max_length=500, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.RESTRICT, null=True, blank=True)
    building_block_necessities = models.TextField(blank=True, null=True)
    building_block_type = models.CharField(
        max_length=20,
        choices=BuildingBlockType.choices,
    )
    is_sensitive = models.BooleanField(default=False)
    # Boolean that is only active for the special empty template that is generated in migration
    is_default_empty = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean(self):
        if self.building_block_type == BuildingBlockType.THEMATIC:
            if not self.theme:
                raise ValidationError("A building block of type %s needs a theme" % BuildingBlockType.THEMATIC.label)
            if self.category:
                raise ValidationError(
                    "A building block of type %s can't have a category" % BuildingBlockType.THEMATIC.label
                )

        if self.building_block_type == BuildingBlockType.METHODIC:
            if not self.category:
                raise ValidationError(
                    "A building block of type %s needs a category" % BuildingBlockType.METHODIC.label
                )
            if self.theme:
                raise ValidationError(
                    "A building block of type %s can't have a theme" % BuildingBlockType.METHODIC.label
                )
