# pylint: disable=unused-argument
"""apps.workshops.api.views.enum_views.building_block_status_viewset."""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from apps.workshops.api.serializers.enum_serializers import EnumOutputSerializer
from apps.workshops.models.enums import BuildingBlockStatus


class BuildingBlockStatusViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(BuildingBlockStatus.choices, many=True)
        return Response(serializer.data)
