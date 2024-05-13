# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module scouts_wwdb_api.wsgi."""


def test_wsgi():
    import django

    from scouts_wwdb_api.wsgi import application

    assert application is not None
    assert isinstance(application, django.core.handlers.wsgi.WSGIHandler)
