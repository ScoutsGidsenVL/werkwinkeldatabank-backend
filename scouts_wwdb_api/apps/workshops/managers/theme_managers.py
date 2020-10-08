from django.db import models
from apps.base.managers import DisabledFieldQuerySetMixin


class ThemeQuerySet(DisabledFieldQuerySetMixin, models.QuerySet):
    def allowed(self, user):
        return self.disabled_allowed(user)


class ThemeManager(models.Manager):
    def get_queryset(self):
        return ThemeQuerySet(self.model, using=self._db)
