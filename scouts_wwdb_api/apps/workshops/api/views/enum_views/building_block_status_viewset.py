from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from ....models.enums import BuildingBlockStatus
from ...serializers.enum_serializers import EnumOutputSerializer


class BuildingBlockStatusViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(BuildingBlockStatus.choices, many=True)
        return Response(serializer.data)
