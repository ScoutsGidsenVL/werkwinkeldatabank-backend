"""apps.workshops.models.enums.building_block_status."""

from django.db import models


class BuildingBlockStatus(models.TextChoices):
    PRIVATE = "PRIVATE", "Privé"
    PUBLICATION_REQUESTED = "PUBLICATION_REQUESTED", "Publicatie aangevraagd"
    PUBLISHED = "PUBLISHED", "Gepubliceerd"
