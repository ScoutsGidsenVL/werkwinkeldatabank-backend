"""apps.workshops.admin.

see https://codinggear.org/how-to-register-model-in-django-admin/

"""
import itertools as it 

import django

# import apps.workshops.models as workshops_models
# django.contrib.admin.site.register(workshops_models.Workshop)
# django.contrib.admin.site.register(workshops_models.Theme)

models = it.chain(
    # django.apps.apps.get_app_config("base").get_models(),
    django.apps.apps.get_app_config("files").get_models(),
    django.apps.apps.get_app_config("scouts_auth").get_models(),
    django.apps.apps.get_app_config("workshops").get_models(),
)


# models = django.apps.apps.get_models()

for model in models:
    try:
        django.contrib.admin.site.register(model)
    except django.contrib.admin.sites.AlreadyRegistered:  # pragma: no cover
        pass
