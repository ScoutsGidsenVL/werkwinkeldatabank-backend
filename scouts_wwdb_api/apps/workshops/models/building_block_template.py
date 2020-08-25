from django.db import models
from .abstract.abstract_building_block import AbstractBuildingBlock
from .enums.building_block_type import BuildingBlockType


# This model represents a template for a building block that can be used by scouts admins to manage some predefined templates
# These are not actual building blocks and cant be connected directly to a workshop
class BuildingBlockTemplate(AbstractBuildingBlock):
    building_block_type = models.CharField(max_length=20, choices=BuildingBlockType.choices,)

    def __str__(self):
        return self.title
