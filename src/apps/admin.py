"""apps.admin."""
import django

import apps.workshops.models as workshops_models

django.contrib.admin.site.register(workshops_models.Workshop)
django.contrib.admin.site.register(workshops_models.Theme)
