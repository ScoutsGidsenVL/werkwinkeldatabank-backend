"""apps.workshops.models.enums.workshop_status_type."""

from django.db import models


class WorkshopStatusType(models.TextChoices):
    PRIVATE = "PRIVATE", "Privé"
    PUBLICATION_REQUESTED = "PUBLICATION_REQUESTED", "Publicatie aangevraagd"
    PUBLISHED = "PUBLISHED", "Gepubliceerd"
