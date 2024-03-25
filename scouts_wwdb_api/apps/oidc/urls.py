"""apps.oidc.urls."""
from django.urls import path

from apps.oidc.api.views import AuthCodeView, RefreshView

urlpatterns = [
    path("token/", AuthCodeView.as_view()),
    path("refresh/", RefreshView.as_view()),
]
