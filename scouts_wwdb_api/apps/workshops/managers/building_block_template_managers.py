from django.db import models
from apps.base.managers import DisabledFieldQuerySetMixin


class BuildingBlockTemplateQuerySet(DisabledFieldQuerySetMixin, models.QuerySet):
    def non_empty(self):
        return self.filter(is_default_empty=False)

    def allowed(self, user):
        return self.disabled_allowed(user)


class BuildingBlockTemplateManager(models.Manager):
    def get_queryset(self):
        return BuildingBlockTemplateQuerySet(self.model, using=self._db)

    def get_empty_default(self):
        return self.get_queryset().filter(is_default_empty=True).first()
