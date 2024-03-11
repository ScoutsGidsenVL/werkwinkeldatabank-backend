# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module scouts_wwdb_api.settings."""


def test_settings():
    # from scouts_wwdb_api import settings
    import django
    django.setup()

    from django.conf import settings

    assert settings.DEBUG is True

