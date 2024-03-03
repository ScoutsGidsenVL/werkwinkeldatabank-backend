from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.base.models import AuditTimestampMixin, BaseModel, CreatedByMixin, DisabledFieldModelMixin

from ..managers import WorkshopManager
from .enums.scouts_team import ScoutsTeam
from .enums.workshop_status_type import WorkshopStatusType
from .theme import Theme


class Workshop(DisabledFieldModelMixin, AuditTimestampMixin, CreatedByMixin, BaseModel):
    # Need to define objects exlicitly otherwise the default Workshop.objects gets overridden by my_workshops
    objects = WorkshopManager()

    title = models.CharField(max_length=200)
    duration = models.DurationField(default=timedelta())
    themes = models.ManyToManyField(Theme, related_name="workshops")
    description = models.TextField()
    short_description = models.TextField(max_length=500, blank=True)
    necessities = models.TextField(blank=True)
    workshop_status_type = models.CharField(
        max_length=30, choices=WorkshopStatusType.choices, default=WorkshopStatusType.PRIVATE
    )
    approving_team = models.CharField(max_length=30, choices=ScoutsTeam.choices, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)

    # Related Many field
    # These are the related many fields that are opposites of ForeignKey or ManyToMany fields.
    # We add them here in comment for documentation purposes
    #
    # building_blocks (BuildingBlockInstances)
    # historic_data (History)
    # files (CKEditorFile)

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
            ("view_all_workshop", "Can view all workshops"),
            ("change_all_workshop", "Can change all workshops"),
            ("request_publication_workshop", "Can request publication of workshops"),
            ("publish_workshop", "Can publish of workshops"),
            ("unpublish_workshop", "Can unpublish of workshops"),
            ("view_publication_requested_workshop", "Can view the to workshop with the status publication requested"),
            ("view_field_created_by_workshop", "Can view created by field of workshops"),
            ("view_field_is_sensitive_workshop", "Can view is sensitive field of workshops"),
        ]
