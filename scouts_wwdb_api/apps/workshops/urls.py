from django.urls import path, include
from rest_framework import routers
from .api.views.theme_viewset import ThemeViewSet

router = routers.SimpleRouter()
router.register(r"themes", ThemeViewSet, "Theme")

urlpatterns = router.urls
