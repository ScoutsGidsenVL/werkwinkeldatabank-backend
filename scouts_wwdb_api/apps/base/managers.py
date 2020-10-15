from django.db import models


class DisabledFieldQuerySetMixin(models.QuerySet):
    def active(self):
        return self.filter(is_disabled=False)

    def inactive(self):
        return self.filter(is_disabled=True)

    def disabled_allowed(self, user):
        if not user.has_perm("scouts_auth.access_disabled_entities"):
            return self.active()
        return self.filter()


class CreatedByQuerySetMixin(models.QuerySet):
    def owned(self, user):
        return self.filter(created_by=user)
