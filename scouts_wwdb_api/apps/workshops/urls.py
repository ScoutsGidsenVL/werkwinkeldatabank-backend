from django.urls import include, path
from rest_framework import routers

from .api.views.building_block_template_viewset import BuildingBlockTemplateViewSet
from .api.views.category_viewset import CategoryViewSet
from .api.views.enum_views.building_block_status_viewset import BuildingBlockStatusViewSet
from .api.views.enum_views.building_block_type_viewset import BuildingBlockTypeViewSet
from .api.views.enum_views.scouts_team_viewset import ScoutsTeamViewset
from .api.views.enum_views.workshop_status_type_viewset import WorkshopStatusTypeViewSet
from .api.views.theme_viewset import ThemeViewSet
from .api.views.workshop_viewset import WorkshopViewSet

router = routers.SimpleRouter()
router.register(r"themes", ThemeViewSet, "Theme")
router.register(r"workshops", WorkshopViewSet, "Workshop")
router.register(r"categories", CategoryViewSet, "Category")
router.register(r"building_block_templates", BuildingBlockTemplateViewSet, "BuildingBlockTemplate")
router.register(r"building_block_types", BuildingBlockTypeViewSet, "BuildingBlockType")
router.register(r"building_block_statuses", BuildingBlockStatusViewSet, "BuildingBlockStatus")
router.register(r"workshop_status_types", WorkshopStatusTypeViewSet, "WorkshopStatusType")
router.register(r"teams", ScoutsTeamViewset, "Team")

urlpatterns = router.urls
