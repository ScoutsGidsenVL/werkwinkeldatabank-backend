from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta
from .theme import Theme
from apps.base.models import BaseModel
from .theme import Theme
from .enums.workshop_status_type import WorkshopStatusType
from django.conf import settings


class PublishedWorkshopsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(workshop_status_type=WorkshopStatusType.PUBLISHED)


class MyWorkshopsManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(created_by=user)


class PublicationRequestedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(workshop_status_type=WorkshopStatusType.PUBLICATION_REQUESTED)


class Workshop(BaseModel):
    title = models.CharField(max_length=200)
    duration = models.DurationField(blank=True, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.RESTRICT)
    description = models.TextField()
    short_description = models.TextField(max_length=500, blank=True)
    necessities = models.TextField()
    workshop_status_type = models.CharField(
        max_length=30, choices=WorkshopStatusType.choices, default=WorkshopStatusType.PRIVATE
    )

    # Need to define objects exlicitly otherwise the default Workshop.objects gets overridden by my_workshops
    objects = models.Manager()
    published_workshops = PublishedWorkshopsManager()
    my_workshops = MyWorkshopsManager()
    publication_requested_workshops = PublicationRequestedManager()

    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)

    # Related Many field
    # These are the related many fields that are opposites of ForeignKey or ManyToMany fields. We add them here in comment for documentation purposes
    #
    # building_blocks (BuildingBlockInstances)

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.building_blocks.all()) < 1:
            raise ValidationError("A workshop needs at least one building block")
