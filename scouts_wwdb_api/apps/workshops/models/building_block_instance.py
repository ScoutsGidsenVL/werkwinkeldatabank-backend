from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.base.models import BaseModel

from ..models.category import Category
from ..models.theme import Theme
from .building_block_template import BuildingBlockTemplate
from .enums.building_block_type import BuildingBlockType
from .workshop import Workshop


# This model represents the actual instance of a building block and can overwrite many of the fields of the template
class BuildingBlockInstance(BaseModel):
    template = models.ForeignKey(BuildingBlockTemplate, on_delete=models.RESTRICT)
    workshop = models.ForeignKey(Workshop, on_delete=models.RESTRICT, related_name="building_blocks")
    order = models.IntegerField()
    linked_template_values = models.BooleanField(default=False)

    # Properties that can be linked to template or overwritten by instance
    _description = models.TextField(blank=True)
    _title = models.CharField(max_length=200, blank=True)
    _duration = models.DurationField(
        validators=[MinValueValidator(timedelta(minutes=0)), MaxValueValidator(timedelta(days=1))],
        null=True,
        blank=True,
    )
    _category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True)
    _short_description = models.CharField(max_length=500, blank=True)
    _theme = models.ForeignKey(Theme, on_delete=models.RESTRICT, null=True, blank=True)
    _building_block_necessities = models.TextField(blank=True)

    @property
    def title(self):
        if not self.linked_template_values:
            return self._title
        return self.template.title

    # If title, description and duration set empty, allowed if linked template values true.
    # Then we still set them the same as the template values in the database
    # so they are not empty if linked_template_values is ever changed
    @title.setter
    def title(self, value):
        if not value:
            value = self.template.title
        self._title = value

    @property
    def description(self):
        if not self.linked_template_values:
            return self._description
        return self.template.description

    @description.setter
    def description(self, value):
        if not value:
            value = self.template.description
        self._description = value

    @property
    def duration(self):
        if not self.linked_template_values:
            return self._duration
        return self.template.duration

    @duration.setter
    def duration(self, value):
        if value is None:
            value = self.template.duration
        self._duration = value

    @property
    def category(self):
        if not self.linked_template_values:
            return self._category
        return self.template.category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def short_description(self):
        if not self.linked_template_values:
            return self._short_description
        return self.template.short_description

    @short_description.setter
    def short_description(self, value):
        self._short_description = value

    @property
    def theme(self):
        if not self.linked_template_values:
            return self._theme
        return self.template.theme

    @theme.setter
    def theme(self, value):
        self._theme = value

    @property
    def building_block_necessities(self):
        if not self.linked_template_values:
            return self._building_block_necessities
        return self.template.building_block_necessities

    @building_block_necessities.setter
    def building_block_necessities(self, value):
        self._building_block_necessities = value

    def __str__(self):
        return self.title

    # properties that are always from template
    @property
    def building_block_type(self):
        return self.template.building_block_type

    @property
    def is_sensitive(self):
        return self.template.is_sensitive

    class Meta:
        ordering = ["order"]

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
