"""apps.workshops.managers.category_managers."""
from django.db import models

from apps.base.managers import DisabledFieldQuerySetMixin


class CategoryQuerySet(DisabledFieldQuerySetMixin, models.QuerySet):
    def allowed(self, user):
        return self.disabled_allowed(user)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
