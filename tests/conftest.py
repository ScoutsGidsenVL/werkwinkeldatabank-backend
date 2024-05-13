"""contest.py - configuration for pytest.

Examples:
  - https://github.com/DjangoGirls/djangogirls/blob/main/tests/conftest.py
  - https://github.com/CuriousLearner/django-phone-verify/tree/master/tests

"""

import django
import pytest
import rest_framework.test


@pytest.fixture()
def superuser(db):
    from apps.scouts_auth.models import User

    return User.objects.create(
        first_name="Super",
        last_name="Scout",
        email="scout-superuser@example.com",
        is_active=True,
        is_superuser=True,
        is_staff=True,
    )


@pytest.fixture
def client():
    return django.test.Client()


@pytest.fixture
def client_superuser(superuser):
    client_ = django.test.Client()
    client_.force_login(superuser)
    return client_


superuser


@pytest.fixture
def apiclient():
    return rest_framework.test.APIClient()
