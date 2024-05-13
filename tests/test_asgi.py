# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module scouts_wwdb_api.asgi."""


def test_asgi():
    import django

    from scouts_wwdb_api.asgi import application

    assert application is not None
    assert isinstance(application, django.core.handlers.asgi.ASGIHandler)
