# pylint: disable=unused-argument
"""apps.workshops.api.views.enum_views.building_block_type_viewset."""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from apps.workshops.models.enums.building_block_type import BuildingBlockType
from apps.workshops.api.serializers.enum_serializers import EnumOutputSerializer


class BuildingBlockTypeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(BuildingBlockType.choices, many=True)
        return Response(serializer.data)
