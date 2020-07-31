from django.urls import path, include
from rest_framework import routers
from .api.views.theme_viewset import ThemeViewSet
from .api.views.workshop_viewset import WorkshopViewSet

router = routers.SimpleRouter()
router.register(r"themes", ThemeViewSet, "Theme")
router.register(r"workshops", WorkshopViewSet, "Workshop")

urlpatterns = router.urls
