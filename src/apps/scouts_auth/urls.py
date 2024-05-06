"""apps.scouts_auth.urls."""
from django.urls import path

from apps.scouts_auth.api.views import CurrentUserView

urlpatterns = [
    path("me/", CurrentUserView.as_view()),
]
