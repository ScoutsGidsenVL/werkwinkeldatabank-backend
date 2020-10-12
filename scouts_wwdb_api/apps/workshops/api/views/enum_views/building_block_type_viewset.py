from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from ...serializers.enum_serializers import EnumOutputSerializer
from ....models.enums.building_block_type import BuildingBlockType


class BuildingBlockTypeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(BuildingBlockType.choices, many=True)
        return Response(serializer.data)
