# flake8: noqa: E402 (module level import not at top of file)
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
# pylint: disable=invalid-name
"""IPython startup-file, outside of PYTHONPATH.

Files in this startup-folder will be run in lexicographical order,
so you can control the execution order of files with a prefix, e.g.::

    00-foo.py
    10-baz.py
    20-bar.py

return-statements are not allowed.

"""
print(f"Executing {__file__}")

import django
from django.conf import settings

# settings = django.conf.settings

# see https://docs.djangoproject.com/en/4.2/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
django.setup()

# Now this script or any imported module can use any part of Django it needs.
import django.db as db
import django.db.models as models
import django.db.models as django_db_models
import django.contrib.auth.models as django_contrib_auth_models

# import from django.contrib.auth.models import Group

import apps.base.models as base_models
import apps.files.models as files_models
import apps.scouts_auth.models as scouts_auth_models
import apps.workshops.models as workshops_models
