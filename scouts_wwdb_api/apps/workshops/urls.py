from django.urls import path, include
from rest_framework import routers
from .api.views.theme_viewset import ThemeViewSet
from .api.views.workshop_viewset import WorkshopViewSet
from .api.views.category_viewset import CategoryViewSet
from .api.views.building_block_template_viewset import BuildingBlockTemplateViewSet
from .api.views.enum_views.building_block_type_viewset import BuildingBlockTypeViewSet

router = routers.SimpleRouter()
router.register(r"themes", ThemeViewSet, "Theme")
router.register(r"workshops", WorkshopViewSet, "Workshop")
router.register(r"categories", CategoryViewSet, "Category")
router.register(r"building_block_templates", BuildingBlockTemplateViewSet, "BuildingBlockTemplate")
router.register(r"building_block_types", BuildingBlockTypeViewSet, "BuildingBlockType")

urlpatterns = router.urls
