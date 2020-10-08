from django.db import models
from apps.base.managers import DisabledFieldQuerySetMixin
from ..models.enums.workshop_status_type import WorkshopStatusType


class WorkshopQuerySet(DisabledFieldQuerySetMixin, models.QuerySet):
    def allowed(self, user):
        return self.disabled_allowed(user)

    def published(self):
        return self.filter(workshop_status_type=WorkshopStatusType.PUBLISHED)

    def publication_requested(self):
        return self.filter(workshop_status_type=WorkshopStatusType.PUBLICATION_REQUESTED)

    def owned(self, user):
        return self.filter(created_by=user)


class WorkshopManager(models.Manager):
    def get_queryset(self):
        return WorkshopQuerySet(self.model, using=self._db)
