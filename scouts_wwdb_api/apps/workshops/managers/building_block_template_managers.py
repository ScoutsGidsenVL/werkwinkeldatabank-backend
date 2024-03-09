"""apps.workshops.building_block_template_managers."""
from django.db import models
from django.db.models import Q

from apps.base.managers import DisabledFieldQuerySetMixin
from apps.workshops.models.enums import BuildingBlockStatus


class BuildingBlockTemplateQuerySet(DisabledFieldQuerySetMixin, models.QuerySet):
    
    def non_empty(self):
        return self.filter(is_default_empty=False)

    def allowed(self, user):
        return self.disabled_allowed(user).template_allowed(user)

    def template_allowed(self, user):
        # If no user only return published
        if user.is_anonymous:
            return self.published()
        else:
            if user.has_perm("workshops.view_all_buildingblocktemplate"):
                return self.filter()
            elif user.has_perm("workshops.view_publication_requested_buildingblocktemplate"):
                return self.filter(
                    Q(
                        status__in=(
                            BuildingBlockStatus.PUBLISHED,
                            BuildingBlockStatus.PUBLICATION_REQUESTED,
                        )
                    )
                    | Q(created_by=user)
                )
            else:
                return self.filter(Q(status=BuildingBlockStatus.PUBLISHED) | Q(created_by=user))

    def published(self):
        return self.filter(status=BuildingBlockStatus.PUBLISHED)

    def publication_requested(self):
        return self.filter(status=BuildingBlockStatus.PUBLICATION_REQUESTED)


class BuildingBlockTemplateManager(models.Manager):
    def get_queryset(self):
        return BuildingBlockTemplateQuerySet(self.model, using=self._db)

    def get_empty_default(self):
        return self.get_queryset().filter(is_default_empty=True).first()
