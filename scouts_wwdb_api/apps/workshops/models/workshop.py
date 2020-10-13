from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import timedelta
from .theme import Theme
from apps.base.models import BaseModel, DisabledFieldModelMixin, AuditTimestampMixin
from .theme import Theme
from .enums.workshop_status_type import WorkshopStatusType
from .enums.scouts_team import ScoutsTeam
from ..managers import WorkshopManager
from django.conf import settings


class Workshop(DisabledFieldModelMixin, AuditTimestampMixin, BaseModel):
    # Need to define objects exlicitly otherwise the default Workshop.objects gets overridden by my_workshops
    objects = WorkshopManager()

    title = models.CharField(max_length=200)
    duration = models.DurationField(default=timedelta())
    theme = models.ForeignKey(Theme, on_delete=models.RESTRICT)
    description = models.TextField()
    short_description = models.TextField(max_length=500, blank=True)
    necessities = models.TextField(blank=True)
    workshop_status_type = models.CharField(
        max_length=30, choices=WorkshopStatusType.choices, default=WorkshopStatusType.PRIVATE
    )
    approving_team = models.CharField(max_length=30, choices=ScoutsTeam.choices, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )

    # Related Many field
    # These are the related many fields that are opposites of ForeignKey or ManyToMany fields.
    # We add them here in comment for documentation purposes
    #
    # building_blocks (BuildingBlockInstances)
    # historic_data (History)

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.building_blocks.all()) < 1:
            raise ValidationError("A workshop needs at least one building block")

        if self.workshop_status_type == WorkshopStatusType.PUBLISHED and not self.approving_team:
            raise ValidationError("A published workshop needs an approving team")

        if self.workshop_status_type == WorkshopStatusType.PUBLISHED and not self.published_at:
            raise ValidationError("A published workshop needs a published at date")

    def calculate_duration(self):
        duration = timedelta()
        for building_block in self.building_blocks.all():
            duration += building_block.duration
        self.duration = duration

    @property
    def is_sensitive(self):
        for building_block in self.building_blocks.all():
            if building_block.is_sensitive:
                return True
        return False

    class Meta:
        permissions = [
            ("view_to_be_published_workshops", "Can view the to be published workshops"),
        ]
