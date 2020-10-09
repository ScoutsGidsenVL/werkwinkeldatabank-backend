from django.db import models


class DisabledFieldModelMixin(models.Model):
    is_disabled = models.BooleanField(default=False)

    class Meta:
        abstract = True
