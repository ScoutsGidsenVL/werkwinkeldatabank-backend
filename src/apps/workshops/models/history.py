"""apps.workshops.models.history."""

from django.core.exceptions import ValidationError
from django.db import models

from apps.base.models import AuditTimestampMixin, BaseModel

from apps.workshops.models.building_block_template import BuildingBlockTemplate
from apps.workshops.models.workshop import Workshop


class History(AuditTimestampMixin, BaseModel):
    data = models.JSONField()
    workshop = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="historic_data", blank=True, null=True
    )
    building_block = models.ForeignKey(
        BuildingBlockTemplate, on_delete=models.CASCADE, related_name="historic_data", blank=True, null=True
    )

    def clean(self):
        if not self.workshop and not self.building_block:
            raise ValidationError("History needs to be related to either workshop or building block")
