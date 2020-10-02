from django.db import models
from .abstract.abstract_building_block import AbstractBuildingBlock
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from .building_block_template import BuildingBlockTemplate
from .workshop import Workshop
from ..models.category import Category
from ..models.theme import Theme

# This model represents the actual instance of a building block and can overwrite many of the fields of the template
class BuildingBlockInstance(AbstractBuildingBlock):
    template = models.ForeignKey(BuildingBlockTemplate, on_delete=models.RESTRICT)
    workshop = models.ForeignKey(Workshop, on_delete=models.RESTRICT, related_name="building_blocks")

    _description = models.TextField(blank=True)
    _title = models.CharField(max_length=200, blank=True)
    _duration = models.DurationField(
        validators=[MinValueValidator(timedelta(minutes=1)), MaxValueValidator(timedelta(days=1))],
        null=True,
        blank=True,
    )
    _category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True)
    _short_description = models.CharField(max_length=500, blank=True)
    _theme = models.ForeignKey(Theme, on_delete=models.RESTRICT, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    _buildingblock_necessities = models.TextField(blank=True)
    _is_sensitive = models.BooleanField(default=False, null=True, blank=True)

    @property
    def title(self):
        if self._title:
            return self._title
        return self.template.title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        if self._description:
            return self._description
        return self.template.description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def duration(self):
        if self._duration:
            return self._duration
        return self.template.duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def category(self):
        if self._category:
            return self._category
        return self.template.category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def short_description(self):
        if self._short_description:
            return self._short_description
        return self.template.short_description

    @short_description.setter
    def short_description(self, value):
        self._short_description = value

    @property
    def theme(self):
        if self._theme:
            return self._theme
        return self.template.theme

    @theme.setter
    def theme(self, value):
        self._theme = value

    @property
    def buildingblock_necessities(self):
        if self._buildingblock_necessities:
            return self._buildingblock_necessities
        return self.template.buildingblock_necessities

    @buildingblock_necessities.setter
    def buildingblock_necessities(self, value):
        self._buildingblock_necessities = value

    @property
    def is_sensitive(self):
        if self._is_sensitive:
            return self._is_sensitive
        return self.template.is_sensitive

    @is_sensitive.setter
    def is_sensitive(self, value):
        self._is_sensitive = value

    def __str__(self):
        return self.title

    @property
    def building_block_type(self):
        return self.template.building_block_type
