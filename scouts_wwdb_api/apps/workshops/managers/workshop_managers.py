"""apps.workshops.managers.workshop_managers."""
from django.db import models
from django.db.models import Q

from apps.base.managers import CreatedByQuerySetMixin, DisabledFieldQuerySetMixin
from apps.workshops.models.enums.workshop_status_type import WorkshopStatusType


class WorkshopQuerySet(DisabledFieldQuerySetMixin, CreatedByQuerySetMixin, models.QuerySet):
    def allowed(self, user):
        return self.disabled_allowed(user).workshop_allowed(user)

    def workshop_allowed(self, user):
        # If no user only return published
        if user.is_anonymous:
            return self.published()
        else:
            if user.has_perm("workshops.view_all_workshop"):
                return self.filter()
            elif user.has_perm("workshops.view_publication_requested_workshop"):
                return self.filter(
                    Q(
                        workshop_status_type__in=(
                            WorkshopStatusType.PUBLISHED,
                            WorkshopStatusType.PUBLICATION_REQUESTED,
                        )
                    )
                    | Q(created_by=user)
                )
            else:
                return self.filter(Q(workshop_status_type=WorkshopStatusType.PUBLISHED) | Q(created_by=user))

    def published(self):
        return self.filter(workshop_status_type=WorkshopStatusType.PUBLISHED)

    def publication_requested(self):
        return self.filter(workshop_status_type=WorkshopStatusType.PUBLICATION_REQUESTED)


class WorkshopManager(models.Manager):
    def get_queryset(self):
        return WorkshopQuerySet(self.model, using=self._db)
