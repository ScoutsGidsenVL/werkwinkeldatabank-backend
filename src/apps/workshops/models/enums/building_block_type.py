"""apps.workshops.models.enums.building_block_type."""
from django.db import models


class BuildingBlockType(models.TextChoices):
    THEMATIC = "THEMATIC", "Inhoud"
    METHODIC = "METHODIC", "Werkvorm"
