# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module scouts_wwdb_api.settings."""

import pytest


def test_settings():
    # from scouts_wwdb_api import settings
    # see https://docs.djangoproject.com/en/4.2/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage

    import django
    from django.conf import settings

    django.setup()

    assert settings.DEBUG is True  # see django_debug_mode-setting
    assert settings.AUTH_USER_MODEL == "scouts_auth.User"


@pytest.mark.urls("scouts_wwdb_api.urls")
def test_swagger_url(client):
    assert b"Scouts WWDB API" in client.get("/swagger/").content
    assert b"Scouts WWDB API" in client.get("/swagger/").content
