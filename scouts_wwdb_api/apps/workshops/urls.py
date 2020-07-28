from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThemeDetailApi

theme_patterns = [
    path("<theme_id>/", ThemeDetailApi.as_view(), name="detail"),
]

urlpatterns = [
    path("themes/", include((theme_patterns, "themes"))),
]
