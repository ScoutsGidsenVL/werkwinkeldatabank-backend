from django.db import models


class BuildingBlockTemplateManager(models.Manager):
    def all_non_empty(self):
        return super().get_queryset().filter(is_default_empty=False)

    def get_empty_default(self):
        return super().get_queryset().filter(is_default_empty=True).first()
