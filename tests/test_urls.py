# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module scouts_wwdb_api.urls."""

import django


def test_urls(client, client_superuser):

    resp = client.get("/admin/")
    assert resp.status_code == 302
    assert resp.url == "/admin/login/?next=/admin/"

    resp = client.get("/admin/login/?next=/admin/")
    assert resp.status_code == 200
    assert resp.context_data["view"].template_name == "admin/login.html"

    resp = client.get("/api/auth/me/")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Authentication credentials were not provided."}

    # resp = client_superuser.get("/api/auth/me/")
    # assert resp.status_code == 401
    # assert resp.json() == {"detail": "Authentication credentials were not provided."}

    resp = client.get("/swagger/")
    assert resp.status_code == 200
    assert resp.context["view"].get_view_name() == "Schema"

    # assert resp.context_data["view"].template_name == "drf_yasg/swagger-ui.html"

    resp = client.get("/redoc/")
    assert resp.status_code == 200
    assert resp.status_text == "OK"
    assert resp.context["view"].get_view_name() == "Schema"

    # with django.test.override_settings(DEBUG=True):
    #     # resp = client.get("/__debug__/")
    #     # assert resp.status_code == 404
    #     assert ['127.0.0.1'] in django.conf.settings.INTERNAL_IPS

    with django.test.override_settings(DEBUG=False):
        # resp = client.get("/__debug__/")
        # assert resp.status_code == 404
        assert ["127.0.0.1"] not in django.conf.settings.INTERNAL_IPS
