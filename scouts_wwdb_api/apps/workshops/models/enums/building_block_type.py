from django.db import models


class BuildingBlockType(models.TextChoices):
    THEMATIC = "THEMATIC", "Thematisch"
    METHODIC = "METHODIC", "Methodisch"
