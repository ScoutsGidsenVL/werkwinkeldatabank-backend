from django.db import models
from .abstract.abstract_building_block import AbstractBuildingBlock
from .building_block_template import BuildingBlockTemplate

# This model represents the actual instance of a building block and can overwrite many of the fields of the template
class BuildingBlockInstance(AbstractBuildingBlock):
    template = models.ForeignKey(BuildingBlockTemplate, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title
