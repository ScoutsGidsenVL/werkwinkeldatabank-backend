from django.db import models


class BuildingBlockType(models.TextChoices):
    THEMATIC = "THEMATIC", "Inhoud"
    METHODIC = "METHODIC", "Werkvorm"
